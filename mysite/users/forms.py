from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from polls.models import Poll


class MemberForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

# class ChangePasswordForm(UserCreationForm):
#     old_password = forms.CharField(widget=forms.PasswordInput())
#     new_password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three','posted_by']
