from django.contrib import admin
from django.db import models
from .models import Mission, Task, UserProfile, Priority, Priority_Mission
from django.contrib.auth.models import User
# Register your models here.

class MissionAdmin(admin.ModelAdmin):
    list_display = ['name','description','belongs_to']

    class Meta:
        model = Mission

class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

    class Meta:
        model = Task

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user","totalexp","supervisor"]

admin.site.register(Mission, MissionAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Priority)
admin.site.register(Priority_Mission)
admin.site.register(UserProfile, UserProfileAdmin)
