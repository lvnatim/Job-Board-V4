from __future__ import unicode_literals
from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    totalexp = models.IntegerField(default=0)
    supervisor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

#User Form
class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username: ")
    first_name = forms.CharField(help_text="First Name: ")
    last_name = forms.CharField(help_text="Last Name: ")
    email = forms.CharField(help_text="Email: ")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password :")

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password")

class Mission(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    belongs_to= models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MissionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), help_text="Title of Mission: ")
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), help_text="Brief Description of Mission: ")

    class Meta:
        model = Mission
        fields = ("name","description")


class Task(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    exp = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    belongs_to = models.ForeignKey(Mission, on_delete=models.CASCADE)
    users_enrolled = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name

class TaskForm(forms.ModelForm):
    name = forms.CharField(help_text="Name of task: ")
    description = forms.CharField(widget=forms.Textarea, help_text="Description of task: ")
    exp = forms.IntegerField(help_text="Exp awarded (around 1 point per minute of estimated work): ")

    class Meta:
        model = Task
        fields = ("name","description","exp")
