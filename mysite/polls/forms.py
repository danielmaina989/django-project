from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import MemberForm


class SignUpForm(ModelForm):
    class Meta:
        model = MemberForm
        fields = ['username','first_name','last_name','email','password', 'confirm_password']
    #     widget = {
    #         'username':forms.TextInput(attrs={'class': 'form-control'}),
    #         'first_name':forms.TextInput(attrs={'class': 'form-control'}), 
    #         'last_name':forms.TextInput(attrs={'class': 'form-control'}), 
    #         'email': forms.EmailField(widget=forms.EmailInput(attrs={'class': 'forms-control'})),
    #         'password':forms.PasswordInput(attrs={'class': 'form-control'}),  
    #         'confirm_password':forms.PasswordInput(attrs={'class': 'form-control'}),  
    # }


    

