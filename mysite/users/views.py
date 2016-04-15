from .appfunctions import getLevel
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from missions.models import Mission, MissionForm, Task, TaskForm, UserProfile, UserForm

# Functions that make repeated shit easier
@login_required
def getUserProfile(request):
    user=request.user
    if user.is_authenticated:
        userprofile = UserProfile.objects.get(user=request.user)
        return userprofile
    else:
        return None

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if form.is_valid() and password1 == password2:
            user = form.save()
            user.set_password(user.password)
            user.save()
            UserProfile.objects.create(user=user)
            return HttpResponseRedirect('/accounts/login')
        else:
            return render(request, 'users/register.html', {"form":form,"message":True})
    else:
        form = UserForm()
    return render(request, 'users/register.html', {"form":form})

@login_required
def profile(request):
    userprofile = getUserProfile(request)
    userdict = getLevel(userprofile.totalexp)
    return render(request, 'users/profile.html',{'userdict':userdict,'userprofile':userprofile})

@login_required
def my_quests(request):
    user = getUserProfile(request)
    quests = user.task_set.filter(completed=False)
    return render(request, 'users/my_quests.html', {"quests":quests})

@login_required
def my_missions(request):
    user = getUserProfile(request)
    missions = Mission.objects.filter(belongs_to=user)
    return render(request, 'users/my_missions.html', {"missions":missions})


@login_required
@permission_required('missions.add_mission', raise_exception=True)
def list_tasks(request, id):
    miss = Mission.objects.get(id=id)
    user = getUserProfile(request)
    tasks = Task.objects.filter(belongs_to=miss)
    if miss.belongs_to != user:
        return HttpResponseRedirect(reverse('users:my_missions'))
    else:
        return render(request, 'users/list_tasks.html', {"tasks":tasks, "mission":miss})

@login_required
def remove_task(request, id):
    task = Task.objects.get(id=id)
    miss_id = task.belongs_to.id
    current_profile = getUserProfile(request)
    if current_profile in task.users_enrolled.all():
        current_profile.task_set.remove(task)
        current_profile.save()
        return list_tasks(request, miss_id)
    else:
        return list_tasks(request, miss_id)

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def create_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            mission = form.save(commit=False)
            mission.belongs_to = request.user.userprofile
            mission.save()
            return HttpResponseRedirect('/users/dashboard/')
        else:
            return render(request, 'users/createmission.html/', {'form':form})
    else:
        form = MissionForm()
    return render(request, 'users/createmission.html/', {'form':form})

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def delete_mission(request, id):
    mission = Mission.objects.get(id=id)
    mission.delete()
    return HttpResponseRedirect(reverse('users:my_missions'))


@login_required
@permission_required('missions.add_mission', raise_exception=True)
def create_task(request, id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.belongs_to = Mission.objects.get(id=id)
            task.save()
            return list_tasks(request, id)
        else:
            return render(request, 'users/createtask.html', {"form":form,"mission":mission})
    else:
        form = TaskForm()
        mission = Mission.objects.get(id=id)
        return render(request, 'users/createtask.html', {"form":form,"mission":mission})

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return HttpResponseRedirect(reverse('users:list_tasks',kwargs={"id":task.belongs_to.id}))

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def complete_task(request, id):
    task = Task.objects.get(id=id)
    if task.completed==False:
        for user in task.users_enrolled.all():
            user.totalexp += task.exp
            user.save()
    task.completed=True
    task.save()
    return list_tasks(request, task.belongs_to.id)

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def uncomplete_task(request, id):
    task = Task.objects.get(id=id)
    task.completed=False
    task.save()
    return list_tasks(request, task.belongs_to.id)

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def remove_user(request, id, id2):
    task = Task.objects.get(id=id)
    user = UserProfile.objects.get(id=id2)
    task.users_enrolled.remove(user)
    task.save()
    return list_tasks(request, task.belongs_to.id)

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def edit_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return list_tasks(request, task.belongs_to.id)
        else:
            return render(request, 'users/edit_task.html', {"form":form,"task":task})
    else:
        form = TaskForm(instance=task)
        return render(request, 'users/edit_task.html', {"form":form,"task":task})

def edit_mission(request,id):
    mission = Mission.objects.get(id=id)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            return list_tasks(request, id)
        else:
            return render(request, 'users/edit_mission.html', {"form":form, "mission":mission})
    else:
        form = MissionForm(instance=mission)
        return render(request, 'users/edit_mission.html', {"form":form, "mission":mission})
