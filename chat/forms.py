# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Response
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'required': True,
                'placeholder': 'lisa@example.com',
                'autofocus': True
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'lisamora',
            })
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'placeholder': 'password'}
        self.fields['password2'].widget.attrs = {'placeholder': 'confirm password'}



class NewQuestionForm(forms.ModelForm):
 
    masques = forms.BooleanField(required=False, label = 'Click', initial=False,                                  
                                 disabled=False)
    class Meta:
        model = Question
        fields = ['title', 'body', 'masques']        
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'Please type your question'
            })             
        }  
        

class NewResponseForm(forms.ModelForm):
    masques = forms.BooleanField(required=False, label = 'Click', initial=False,                                
                                 disabled=False)
    class Meta:
        model = Response
        fields = ['body', 'masques']

class EmailNotifForm(forms.Form):
    email_notif = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'this.form.submit();'}),required=False, label="Notify me for new questions in this QA room")
