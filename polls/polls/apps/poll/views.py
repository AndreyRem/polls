from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .models import Poll, Question, Answer, UserAnswer
from polls.apps.auth_service.models import ExtUser
from django.db.models import Count, Sum
from django.views import generic


class PollListView(generic.ListView):
    template_name = 'polls.html'

    def get_queryset(self):
        if 'user_id' in self.kwargs:
            return Poll.objects.filter(owner__id=self.kwargs['user_id']).order_by('-successful_completion_count')
        else:
            return Poll.objects.all()


class PollDetailView(generic.DetailView):
    model = Poll
    template_name = 'poll.html'
    slug_field = 'slug'

    def get_object(self):
        poll_object = super(PollDetailView, self).get_object()
        if self.request.user.is_authenticated():
            poll_object.not_successful_completion_count += 1
            poll_object.save()
        return poll_object

    def post(self, request, *args, **kwargs):
        if 'answer_id' in request.POST:
            answer = Answer.objects.get(pk=request.POST.get('answer_id'))
            answer.selection_count += 1
            question = answer.question
            question.respondents_count += 1
            user = request.user
            if request.POST.get('checked') == 'true':
                if UserAnswer.objects.filter(answer=answer, question=question, user=user).count() == 0:
                    UserAnswer.objects.create(answer=answer, question=question, user=user).save()
            else:
                UserAnswer.objects.filter(answer=answer, question=question, user=user).delete()
            answer.save()
            question.save()
            return HttpResponse('answer_saved')


class SystemStatisticsTemplateView(generic.TemplateView):
    template_name = 'system_statistics.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['users_count'] = ExtUser.objects.all().count()
        context['polls_count'] = Poll.objects.all().count()
        context['successful_completion_count_sum'] = Poll.objects.\
            aggregate(Sum('successful_completion_count'))['successful_completion_count__sum']
        context['most_popular_users'] = ExtUser.objects.annotate(num_polls=Count('poll')).order_by('-num_polls')[:3]
        context['most_popular_polls'] = Poll.objects.order_by('successful_completion_count')[:3]

        return context


def add_poll(request):
    # Добавляет опрос в базу
    # Очень неудачная функция
    poll = Poll(title=request.POST.get('title'), slug=request.POST.get('slug'), owner=request.user, weight=request.POST.get('weight'))
    poll.save()
    post_keys = list(request.POST.keys())
    post_keys.remove('csrfmiddlewaretoken')
    post_keys.remove('title')
    post_keys.remove('slug')
    post_keys.remove('weight')
    post_keys.sort(reverse=True)
    questions_count = len(post_keys) // 2
    for i in range(questions_count):
        question = Question(title=request.POST.get('question_%s' % i), poll=poll)
        question.save()

        answers_titles = request.POST.getlist('answer_for_question_%s' % i)
        for answer_title in answers_titles:
            answer = Answer(title=answer_title, question=question)
            answer.save()
    return redirect('/')


def add_completion_of_poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    poll.successful_completion_count += 1
    poll.not_successful_completion_count -= 1
    poll.save()
    return redirect('/')