from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, FacultyProfile
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'password1', 'password2')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = []  # add 'roll_number', etc. if you have

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = []  # add extra fields if you have



class CustomUserEditForm(UserChangeForm):
    password = None  # hide password from the form

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'first_name', 'last_name', 'phone_number','gender','date_of_birth','address')