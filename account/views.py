from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import UserRegistrationForm, CreationProfileForm, CreationUserForm, LoginForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from friends.models import FriendList


class LoginView(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm

    def get_success_url(self):
        success_url = reverse_lazy('account:profile', kwargs={'username': self.request.user.username})
        return success_url


class RegisterView(generic.CreateView):
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')
    form_class = UserRegistrationForm


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreationView(generic.View, LoginRequiredMixin):
    template_name = 'account/user_creation.html'

    def post(self, request):
        creation_profile_form = CreationProfileForm(request.POST)
        creation_user_form = CreationUserForm(request.POST, use_required_attribute=False)
        if creation_profile_form.is_valid() or creation_user_form.is_valid():
            profile = Profile.objects.get(user=request.user)
            user = User.objects.get(username=request.user)
            if request.POST['first_name']:
                user.first_name = request.POST['first_name']
            if request.POST['last_name']:
                user.last_name = request.POST['last_name']
            if request.POST['date_of_birth']:
                profile.date_of_birth = request.POST['date_of_birth']
            if request.POST['town']:
                profile.town = request.POST['town']
            if request.FILES.get('profile_pic', False):
                profile.profile_pic = request.FILES['profile_pic']
            user.save()
            profile.save()
        messages.success(request, 'Your profile was successfully updated')
        return HttpResponseRedirect(reverse('account:profile', kwargs={'username': user.username}))

    def get(self, request):
        creation_user_form = CreationUserForm
        creation_profile_form = CreationProfileForm
        return render(request,
                      self.template_name,
                      {'creation_form': creation_profile_form,
                       'user_form': creation_user_form})


class LogoutView(LogoutView):
    template_name = 'account/logout.html'

    def get(self, request):
        messages.success(request, 'You are logged out')
        return render(request, 'account/logout.html', {})


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change.html'

    def get_success_url(self):
        messages.success(self.request, 'Your password was successfully changed')
        success_url = reverse_lazy('testApp:profile', kwargs={'username': self.request.user.username})
        return success_url


class ProfileView(generic.DetailView, LoginRequiredMixin):
    template_name = 'account/profile.html'
    context_object_name = 'user_profile'
    slug_field = "username"
    template_name_suffix = '_profile'

    def get(self, request, username):
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=User.objects.get(username=username).id)
        output = {'user_profile': user,
                  'profile_profile': profile, }
        friends = [str(el.friend) for el in FriendList.objects.filter(user=request.user)]
        if username in friends:
            output['friend'] = username
        return self.render_to_response(output)
