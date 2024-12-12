from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']  # Include the fields you want to upload

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']