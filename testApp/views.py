from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Question, Choice, QuestionVoted
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F


def printer():
    now = datetime.datetime.now()
    if 6 < now.hour <= 12:
        param = 'morning'
    elif 12 < now.hour <= 18:
        param = 'day'
    elif 18 < now.hour <= 24:
        param = 'evening'
    else:
        param = 'night'
    return param


class FirstView(generic.ListView):
    template_name = 'testApp/first.html'
    context_object_name = 'latest_question_list'
    queryset = Question.objects.order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(FirstView, self).get_context_data(**kwargs)
        context['text'] = 'Good {0}, dear friend!'.format(printer())
        popular = (Choice.objects.values(question_number=F('question'),
                                         question_text=F('question__question_text'))
                   .annotate(sum_of_votes=Sum('votes'))) \
            .order_by('-sum_of_votes', )
        context['popular'] = popular
        return context


class DetailView(generic.DetailView):
    model = Question

    def get_template_names(self):
        choices = QuestionVoted.objects.filter(question=self.kwargs['pk'], user=self.request.user)
        if choices:
            return 'testApp/results.html'
        else:
            return 'testApp/detail.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST.get('choice', False))
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'testApp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        question_voted = QuestionVoted()
        question_voted.user = request.user
        question_voted.question = question
        question_voted.choice_text = selected_choice.choice_text
        question_voted.save()
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('testApp:results', args=(question.id,)))


def to_main(request):
    if request:
        return HttpResponseRedirect(reverse('testApp:first'))
    else:
        return HttpResponse('There is no request :(')


class AddQuestionView(generic.edit.CreateView, LoginRequiredMixin):
    template_name = 'testApp/add_question.html'
    model = Question
    fields = ['question_text',
              ]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('testApp:my_questions',
                                            kwargs={'username': self.request.user.username}))


class AddChoiceView(generic.edit.CreateView, LoginRequiredMixin):
    template_name = 'testApp/add_choice.html'
    model = Choice
    fields = ['choice_text',
              ]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.question_id = self.kwargs['pk']
        self.object.save()
        return HttpResponseRedirect(reverse('testApp:my_questions',
                                            kwargs={'username': self.request.user.username}))


class MyQuestionView(generic.ListView, LoginRequiredMixin):
    template_name = 'testApp/my_questions.html'
    context_object_name = 'my_questions_list'

    def get_queryset(self):
        queryset = Question.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyQuestionView, self).get_context_data(**kwargs)
        context['choices'] = Choice.objects.filter(user=self.request.user)
        return context


class UpdateMyQuestionView(generic.edit.UpdateView, LoginRequiredMixin):
    template_name = 'testApp/update_question.html'
    model = Question
    fields = ['question_text']

    def get_success_url(self):
        success_url = reverse_lazy('testApp:my_questions', kwargs={'username': self.request.user.username})
        return success_url


class DeleteMyQuestionView(generic.edit.DeleteView, LoginRequiredMixin):
    template_name = 'testApp/delete_question.html'
    model = Question

    def get_success_url(self):
        success_url = reverse_lazy('testApp:my_questions', kwargs={'username': self.request.user.username})
        return success_url


class UpdateChoiceView(generic.edit.UpdateView, LoginRequiredMixin):
    template_name = 'testApp/update_choice.html'
    model = Choice
    fields = ['choice_text']

    def get_success_url(self):
        success_url = reverse_lazy('testApp:my_questions', kwargs={'username': self.request.user.username})
        return success_url


class DeleteChoiceView(generic.edit.DeleteView, LoginRequiredMixin):
    template_name = 'testApp/delete_choice.html'
    model = Choice

    def get_success_url(self):
        success_url = reverse_lazy('testApp:my_questions', kwargs={'username': self.request.user.username})
        return success_url
