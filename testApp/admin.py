from django.contrib import admin
from .models import Question, Choice, QuestionVoted


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'user', 'pub_date')


class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'user', 'votes')


class QuestionVotedAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'choice_text')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, QuestionChoiceAdmin)
admin.site.register(QuestionVoted, QuestionVotedAdmin)


