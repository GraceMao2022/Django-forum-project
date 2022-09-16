from django import forms
from courses.models import Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Profile
from django.conf import settings


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
   
    
# Sign Up Form
class UserRegisterForm(UserCreationForm):
    def custom_validate_email(value):
        if not (value.lower().endswith('fuhsd.org') or value.lower() in settings.GUEST_EMAIL_LIST):
            raise ValidationError('Only school email address is accepted')

    username = forms.CharField(max_length=254, help_text='Enter the part of your school email address before the @')
    email = forms.EmailField(max_length=254, help_text='Enter your school email address', validators=[validate_email, custom_validate_email])

    class Meta:
        model = User
        fields = [
            'username',
            'email', 
            'password1', 
            'password2', 
            ]

# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'user',
            'email_confirmed',
            ]

class SettingsForm(forms.ModelForm):
    receive_response_notif = forms.BooleanField(required=False, label="Notify me if there is a new response to my questions")
    class Meta:
        model = Profile
        fields = [
            'receive_response_notif'
            ]
