from django import forms 
from web_app import models
from django.core.exceptions import ValidationError



class RegisterForm(forms.ModelForm): 
    
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100, required=True)

    class Meta: 
        model = models.User
        fields = ['email', 'password']


class LoginForm(forms.Form):

    email = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100, required=True) 

    
