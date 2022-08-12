from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import FriendRequest, FriendList
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreationUserForm


class MyFriendRequestList(generic.ListView, LoginRequiredMixin):
    template_name = 'friends/my_friend_request.html'
    context_object_name = 'my_friend_request'

    def get_queryset(self):
        queryset = FriendRequest.objects.filter(to_user=self.request.user)
        return queryset


class MySentFriendRequestList(generic.ListView, LoginRequiredMixin):
    template_name = 'friends/my_sent_request.html'
    context_object_name = 'my_sent_request'

    def get_queryset(self):
        queryset = FriendRequest.objects.filter(from_user=self.request.user)
        return queryset


class MyFriendList(generic.ListView, LoginRequiredMixin):
    template_name = 'friends/my_friend_list.html'
    context_object_name = 'my_friend_list'

    def get_queryset(self):
        queryset = FriendList.objects.filter(user=self.request.user)
        return queryset


class DeleteFriendView(generic.View, LoginRequiredMixin):
    template_name = 'friends/delete_friend.html'
    model = FriendList
    fields = '__all__'

    def post(self, request, pk):
        FriendList.objects.filter(user=request.user, friend=pk).delete()
        FriendList.objects.filter(user=pk, friend=request.user).delete()
        return HttpResponseRedirect(reverse('friends:my_friend_list',
                                            kwargs={'username': self.request.user.username}))


class AcceptFriendRequestView(generic.View, LoginRequiredMixin):
    template_name = 'friends/accept_friend_request.html'
    model = FriendList
    fields = '__all__'

    def post(self, request, pk, *args, **kwargs):
        id_from_user = FriendRequest.objects.get(pk=self.kwargs['pk']).from_user.id
        FriendList(user=request.user,
                   friend=User.objects.get(pk=id_from_user)).save()
        FriendList(user=User.objects.get(pk=id_from_user),
                   friend=request.user).save()
        FriendRequest.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('friends:my_friend_list',
                                            kwargs={'username': self.request.user.username}))


class DeclineFriendRequestView(generic.edit.DeleteView, LoginRequiredMixin):
    template_name = 'friends/decline_friend_request.html'
    model = FriendRequest
    fields = '__all__'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class AllUsersSearchView(LoginRequiredMixin, generic.ListView):
    template_name = 'friends/all_users_search.html'
    model = User
    fields = ['username', 'first_name', 'last_name']
    context_object_name = 'five_last_user_list'
    form_class = CreationUserForm

    def get_queryset(self):
        if self.request.GET.get('search_param'):
            search_param = self.request.GET.get('search_param')
            search_param = ' '.join(search_param.split())
            split_search_param = search_param.split(' ')
            if len(search_param) == 0 or len(split_search_param) > 3:
                queryset = User.objects.none()
                return queryset
            else:
                queryset = User.objects.exclude(username=self.request.user) \
                               .filter(username__in=split_search_param) \
                           | User.objects.exclude(username=self.request.user) \
                               .filter(first_name__in=split_search_param) \
                           | User.objects.exclude(username=self.request.user) \
                               .filter(last_name__in=split_search_param)
                return queryset
        else:
            queryset = User.objects.exclude(username=self.request.user).order_by('pk')[:5]
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllUsersSearchView, self).get_context_data(**kwargs)
        context['list_of_friends'] = [el.friend for el in \
                                      FriendList.objects.filter(user=self.request.user)]
        context['list_of_requests'] = [el.to_user for el in \
                                       FriendRequest.objects.filter(from_user=self.request.user)]
        return context


class SendFriendRequestUserView(generic.View, LoginRequiredMixin):
    template_name = 'friends/send_friend_request.html'
    model = FriendRequest
    fields = '__all__'

    def post(self, request, pk, *args, **kwargs):
        if FriendRequest.objects.filter(from_user=request.user, to_user=User.objects.get(pk=pk)):
            messages.success(request, 'Friend request has already sent')
            return HttpResponseRedirect(reverse('friends:user_search'))
        FriendRequest(from_user=request.user, to_user=User.objects.get(pk=pk)).save()
        messages.success(request, 'Friend request was sent')
        return HttpResponseRedirect(reverse('friends:user_search'))

