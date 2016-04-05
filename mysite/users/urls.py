from django.conf.urls import url
from . import views

app_name='users'

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^dashboard/$', views.mytasks, name="mytasks"),
    url(r'^dashboard/remove/(?P<id>\d+)/$', views.remove_task, name="remove_task"),
    url(r'^createmission/$', views.create_mission, name="create_mission"),
    url(r'^mission/(?P<id>\d+)/list/$', views.list_tasks, name="list_tasks"),
    url(r'^mission/(?P<id>\d+)/add/$', views.create_task, name="create_task"),
    url(r'^task/(?P<id>\d+)/complete/$', views.complete_task, name="complete_task"),
    url(r'^task/(?P<id>\d+)/edit/$', views.edit_task, name="edit_task"),
    url(r'^mission/\d+/task/(?P<id>\d+)/removeuser/(?P<id2>\d+)$', views.remove_user, name="remove_user"),
]
