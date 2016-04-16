from django.conf.urls import url
from . import views

app_name='missions'

urlpatterns = [
    url(r'^leaderboard/$', views.leaderboard, name="leaderboard"),
    url(r'^missions/$', views.list_missions, name="list_missions"),
    url(r'^quests/$', views.list_quests, name="list_quests"),
    url(r'^history/$', views.historyTask, name="history"),
    url(r'^quests/by_priority$', views.quest_by_priority, name="quest_by_priority"),
    url(r'^quests/by_exp$', views.quest_by_exp, name="quest_by_exp"),
    url(r'^quests/by_date$', views.quest_by_date, name="quest_by_date"),
    url(r'^missions/by_priority$', views.miss_by_priority, name="miss_by_priority"),
    url(r'^missions/by_date$', views.miss_by_date, name="miss_by_date"),
    url(r'^missions/(?P<id>\d+)$', views.detail_mission, name="detail_mission"),
    url(r'^missions/(?P<id>\d+)/by_exp$', views.sort_by_exp, name="by_exp"),
    url(r'^missions/(?P<id>\d+)/by_date$', views.sort_by_date, name="by_date"),
    url(r'^missions/(?P<id>\d+)/by_priority$', views.sort_by_priority, name="by_priority"),
    url(r'^task/(?P<id>\d+)/accept$', views.accept_task, name="accept_task"),
]
