from django.contrib import admin
from polls.apps.poll.models import Poll, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'successful_completion_count', 'not_successful_completion_count')
    date_hierarchy = 'created_at'
    inlines = (QuestionInline,)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'poll')
    list_filter = ('poll__title',)
    inlines = (AnswerInline,)

admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
