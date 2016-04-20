from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Mission, Task, UserProfile, User, History_Task
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
def list_missions(request):
    missions = Mission.objects.all()
    return render(request, 'missions/list_missions.html', {"missions":missions})

@login_required
def list_quests(request):
    quests = Task.objects.all()
    return render(request, 'missions/list_quests.html', {"quests":quests})

@login_required
def quest_by_priority(request):
    quests = Task.objects.order_by('-priority')
    return render(request, 'missions/list_quests.html', {"quests":quests})

@login_required
def quest_by_exp(request):
    quests = Task.objects.order_by('-exp')
    return render(request, 'missions/list_quests.html', {"quests":quests})

@login_required
def quest_by_date(request):
    quests = Task.objects.order_by('due_date')
    return render(request, 'missions/list_quests.html', {"quests":quests})

@login_required
def miss_by_priority(request):
    missions = Mission.objects.order_by('-priority')
    return render(request, 'missions/list_missions.html', {"missions":missions})

@login_required
def miss_by_date(request):
    missions = Mission.objects.order_by('due_date')
    return render(request, 'missions/list_missions.html', {"missions":missions})

def historyTask(request):
    entries = History_Task.objects.order_by('-timestamp')
    return render(request, 'missions/history_quest.html', {"entries":entries})

@login_required
def detail_mission(request, id):
    userprofile= UserProfile.objects.get(user=request.user)
    mission= get_object_or_404(Mission, id=id)
    tasks = Task.objects.filter(belongs_to=mission)
    return render(request, 'missions/detail_mission.html', {"tasks":tasks, "mission":mission,"userprofile":userprofile})

def sort_by_exp(request, id):
    userprofile= UserProfile.objects.get(user=request.user)
    mission= get_object_or_404(Mission, id=id)
    tasks = Task.objects.filter(belongs_to=mission).order_by('-exp')
    return render(request, 'missions/detail_mission.html', {"tasks":tasks, "mission":mission,"userprofile":userprofile})

def sort_by_date(request, id):
    userprofile= UserProfile.objects.get(user=request.user)
    mission= get_object_or_404(Mission, id=id)
    tasks = Task.objects.filter(belongs_to=mission).order_by('due_date')
    return render(request, 'missions/detail_mission.html', {"tasks":tasks, "mission":mission,"userprofile":userprofile})

def sort_by_priority(request, id):
    userprofile= UserProfile.objects.get(user=request.user)
    mission= get_object_or_404(Mission, id=id)
    tasks = Task.objects.filter(belongs_to=mission).order_by('-priority')
    return render(request, 'missions/detail_mission.html', {"tasks":tasks, "mission":mission,"userprofile":userprofile})

def leaderboard(request):
    users = UserProfile.objects.order_by('-totalexp')
    return render(request, 'missions/leaderboard.html' ,{"users":users})

@login_required
def accept_task(request, id):
    task = get_object_or_404(Task, id=id)
    current_profile = UserProfile.objects.get(user=request.user)
    if current_profile not in task.users_enrolled.all():
        current_profile.task_set.add(task)
        current_profile.save()
        message = "Mission successfully added!"
        return detail_mission(request, task.belongs_to.id)
    else:
        message = "You've already accepted this task."
        return detail_mission(request, task.belongs_to.id)
