from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . import models


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = models.TestCase
        fields = ['name', 'description', 'author']
        widgets = {'description': forms.Textarea}


class UpdateTestCaseForm(forms.ModelForm):
    class Meta:
        model = models.TestCase
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea}
