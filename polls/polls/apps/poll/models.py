from django.db import models
from polls.apps.auth_service.models import ExtUser


class Poll(models.Model):
    class Meta:
        ordering = ('-weight', '-successful_completion_count',)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    owner = models.ForeignKey(ExtUser)
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.CharField(verbose_name='Адрес', max_length=200, null=True)
    weight = models.FloatField(verbose_name='Вес опроса', default=0)
    successful_completion_count = models.IntegerField(
        verbose_name='Количество успешных прохождений',
        default=0
    )

    not_successful_completion_count = models.IntegerField(
        verbose_name='Количество не полных прохождений',
        default=0
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    class Meta:
        ordering = ('poll', )
        verbose_name = 'Вопрос опроса'
        verbose_name_plural = 'Вопросы опросов'

    poll = models.ForeignKey(Poll)
    title = models.CharField(verbose_name='Вопрос', max_length=200)
    respondents_count = models.IntegerField(
        verbose_name='Количество респондентов',
        default=0
    )

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question)

    title = models.CharField(verbose_name='Ответ', max_length=200)
    selection_count = models.IntegerField(
        verbose_name='Количество выборов данного ответа',
        default=0
    )

    def percentage_of_elections(self):
        elections_count = UserAnswer.objects.filter(answer=self).count()
        if elections_count == 0:
            return 0
        elections_of_this_question = UserAnswer.objects.filter(question=self.question).count()
        return elections_count / (elections_of_this_question / 100)

    def __str__(self):
        return self.title


class UserAnswer(models.Model):
    user = models.ForeignKey(ExtUser)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)