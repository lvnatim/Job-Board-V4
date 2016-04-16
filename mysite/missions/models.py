from __future__ import unicode_literals
from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    totalexp = models.IntegerField(default=0)
    supervisor = models.BooleanField(default=False)

    def __str__(self):
        return self.user

#User Form
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text="Username: ")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text="First Name: ")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text="Last Name: ")
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text="Email: ")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), help_text="Password :")

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password")

class Priority_Mission(models.Model):
    name = models.CharField(max_length=60, null=True)
    color = models.CharField(max_length=7, null=True)

    def __str__(self):
        return self.name

class Mission(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    belongs_to= models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    due_date = models.DateField(default=timezone.now)
    priority = models.ForeignKey(Priority_Mission, null=True)

    def __str__(self):
        return self.name

class MissionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), help_text="Title of Mission: ")
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), help_text="Brief Description of Mission: ")
    priority = forms.ModelChoiceField(queryset=Priority_Mission.objects.all(),widget=forms.Select(attrs={"class":"form-control"}), help_text="Help Needed: ", )
    due_date = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control"}), help_text="Due Date (MM/DD/YYYY): ")

    class Meta:
        model = Mission
        fields = ("name","description","priority")

class Priority(models.Model):
    name = models.CharField(max_length=60, null=True)
    color = models.CharField(max_length=7, null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    exp = models.IntegerField(default=0)
    due_date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    priority = models.ForeignKey(Priority, null=True)
    belongs_to = models.ForeignKey(Mission, on_delete=models.CASCADE)
    users_enrolled = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name

class TaskForm(forms.ModelForm):
    name = forms.CharField(help_text="Name of task: ",widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), help_text="Description of task: ")
    exp = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}), help_text="Exp awarded (around 10 points per minute of estimated work): ")
    due_date = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control"}), help_text="Due Date (MM/DD/YYYY): ")
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(),widget=forms.Select(attrs={"class":"form-control"}), help_text="Priority: ", )

    class Meta:
        model = Task
        fields = ("name","description","exp","due_date","priority")

class History_Task(models.Model):
    task = models.ForeignKey(Task)
    users_enrolled = models.ManyToManyField(UserProfile)
    timestamp = models.DateTimeField(auto_now_add=True)
