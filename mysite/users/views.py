from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from missions.models import Mission, MissionForm, Task, TaskForm, UserProfile, UserForm

# Create your views here.
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
def mytasks(request):
    userprofile = UserProfile.objects.get(user=request.user)
    tasks = userprofile.task_set.all()
    missions = userprofile.mission_set.all()
    return render(request, 'users/mytasks.html', {"tasks":tasks,"missions":missions})


@login_required
@permission_required('missions.add_mission', raise_exception=True)
def create_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid:
            mission = form.save(commit=False)
            mission.belongs_to = request.user.userprofile
            mission.save()
            return HttpResponseRedirect('/users/dashboard/')
        else:
            print form.errors
    else:
        form = MissionForm()
    return render(request, 'users/createmission.html/', {'form':form})

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def create_task(request, id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid:
            task = form.save(commit=False)
            task.belongs_to = Mission.objects.get(id=id)
            task.save()
            return HttpResponseRedirect("/users/dashboard/")
        else:
            print form.errors
    else:
        form = TaskForm()
        mission = Mission.objects.get(id=id)
        return render(request, 'users/createtask.html', {"form":form,"mission":mission})

@login_required
@permission_required('missions.add_mission', raise_exception=True)
def list_tasks(request, id):
    miss = Mission.objects.get(id=id)
    tasks = Task.objects.filter(belongs_to=miss)
    return render(request, 'users/list_tasks.html', {"tasks":tasks, "mission":miss})

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
def complete_task(request, id):
    task = Task.objects.get(id=id)
    if task.completed==False:
        for user in task.users_enrolled.all():
            user.totalexp += task.exp
            user.save()
    task.completed=True
    task.save()
    return list_tasks(request, task.belongs_to.id)
