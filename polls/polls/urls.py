from django.conf.urls import url, include
from django.contrib import admin
from polls.apps.poll import views

urlpatterns = [
    url(r'^auth/', include('polls.apps.auth_service.urls', namespace="auth_service")),
    url(r'^polls/', include('polls.apps.poll.urls', namespace="polls")),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.PollListView.as_view(), name='index'),
    url(r'^system_statistics/$', views.SystemStatisticsTemplateView.as_view(), name='index')
]
