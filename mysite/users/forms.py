from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from polls.models import Poll, Question, Choice


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
    name = forms.CharField(required=True)
    class Meta:
        model = Poll
        fields = ['name','posted_by']

class CreatePollQuizForm(ModelForm):
    pub_date = forms.DateTimeField(required=False)
    class Meta:
        model = Question
        fields = ['question_text','pub_date']

class CreatePollChoicesForm(ModelForm):
    question = forms.CharField(required=False)
    poll = forms.CharField(required=False)
    class Meta:
        model = Choice
        fields = ['choice_text']