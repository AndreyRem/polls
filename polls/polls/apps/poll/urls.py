from django.conf.urls import url
# from polls.apps.poll.views import user_polls, poll, add_completion_of_poll, set_user_answer, new_poll, add_poll
from polls.apps.poll.views import add_completion_of_poll, add_poll
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    # Опросы пользователя
    url(r'user_polls/(?P<user_id>\d+)/$', views.PollListView.as_view(), name='user_polls'),

    # Опрос
    url(r'poll/(?P<pk>\d+)/$', views.PollDetailView.as_view(), name='poll'),

    # Обработка завершения прохождения опрса
    url(r'poll/(?P<poll_id>\d+)/add_completion_of_poll/$', add_completion_of_poll, name='add_completion_of_poll'),

    # Обработка ответа пользователя
    url(r'set_user_answer/$', views.PollDetailView.as_view(), name='set_user_answer'),

    # Загрузка пустой страницы для создания опроса
    url(r'new_poll/$', TemplateView.as_view(template_name='create_poll.html'), name='new_poll'),

    # Сохранение опроса в базу
    url(r'add_poll/$', add_poll, name='add_poll'),

    url(r'(?P<slug>\w+)/$', views.PollDetailView.as_view(), name='poll_with_slug'),
]
