from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import DirectMessageForm
from .models import DirectMessage
from django.contrib.auth.models import User


class MyDirectMessageView(generic.ListView, LoginRequiredMixin):
    template_name = 'communication/my_messages.html'
    context_object_name = 'my_dialogues'

    def get_queryset(self):
        dialogues_ordered = DirectMessage.objects.filter(from_user=self.request.user) \
                            | DirectMessage.objects.filter(to_user=self.request.user)
        ff = dialogues_ordered.values_list('from_user', 'to_user').distinct()
        old_el = (0, 0)
        messages_id = []
        for el in ff:
            if old_el == el[::-1]:
                continue
            else:
                dialogue = DirectMessage.objects.filter(from_user=el[0],
                                                        to_user=el[1],
                                                        ) \
                           | DirectMessage.objects.filter(from_user=el[1],
                                                          to_user=el[0],
                                                          )
                messages_id.append(dialogue.order_by('-date_of_message', '-time_of_message')[0].id)
            old_el = el
        dialogues = DirectMessage.objects.filter(id__in=messages_id)\
                                         .order_by('-date_of_message', '-time_of_message')
        return dialogues


class MyDialogueView(generic.ListView, LoginRequiredMixin):
    template_name = 'communication/my_dialogue.html'
    context_object_name = 'my_dialogue'
    model = DirectMessage
    fields = ['direct_message']

    def get_queryset(self):
        dialogue = DirectMessage.objects.filter(from_user=self.request.user,
                                                to_user=self.kwargs.get('dialogue_with'),
                                                ) \
                   | DirectMessage.objects.filter(from_user=self.kwargs.get('dialogue_with'),
                                                  to_user=self.request.user,
                                                  )
        dialogue_ordered = dialogue.order_by('date_of_message', 'time_of_message')
        return dialogue_ordered

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyDialogueView, self).get_context_data(**kwargs)
        context["dialogue_message_form"] = DirectMessageForm
        return context

    def post(self, request, dialogue_with):
        dialogue_message_form = DirectMessageForm(request.POST)
        if dialogue_message_form.is_valid():
            message = DirectMessage()
            message.from_user = request.user
            message.to_user = User.objects.get(id=dialogue_with)
            message.direct_message = request.POST['direct_message']
            message.save()
        return HttpResponseRedirect(reverse('communication:my_dialogue',
                                            kwargs={'dialogue_with': dialogue_with}))
