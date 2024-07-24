from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class MemberForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)



    

