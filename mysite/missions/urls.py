from django.conf.urls import url
from . import views

app_name='missions'

urlpatterns = [
    url(r'^leaderboard/$', views.leaderboard, name="leaderboard"),
    url(r'^$', views.list_missions, name="list_missions"),
    url(r'^(?P<id>\d+)$', views.detail_mission, name="detail_mission"),
    url(r'^(?P<id>\d+)/by_exp$', views.sort_by_exp, name="by_exp"),
    url(r'^(?P<id>\d+)/by_date$', views.sort_by_date, name="by_date"),
    url(r'^(?P<id>\d+)/by_priority$', views.sort_by_priority, name="by_priority"),
    url(r'^task/(?P<id>\d+)/accept$', views.accept_task, name="accept_task"),
]
