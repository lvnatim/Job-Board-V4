from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Mission, Task

class Form(forms.ModelForm):
    username = forms.CharField(help_text="Username: ")
    first_name = forms.CharField(help_text="First Name: ")
    last_name = forms.CharField(help_text="Last Name: ")
    email = forms.CharField(help_text="Email: ")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password": )

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password")
