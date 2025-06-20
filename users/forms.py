from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, FacultyProfile
from django.contrib.auth.forms import UserChangeForm
from courses.models import Course
from django.contrib.auth.forms import AuthenticationForm
from courses.models import Course
import random
import string

def generate_student_id():
    return 'AGP' + ''.join(random.choices(string.digits, k=6))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=15)
    gender = forms.ChoiceField(choices=User._meta.get_field('gender').choices, required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'gender', 'password1', 'password2', 'course']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 3:
            raise forms.ValidationError("Password must be at least 3 characters long.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'STUDENT'
        user.phone_number = self.cleaned_data['phone_number']
        user.gender = self.cleaned_data['gender']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Generate and ensure unique student_id
            student_id = generate_student_id()
            while StudentProfile.objects.filter(student_id=student_id).exists():
                student_id = generate_student_id()

            StudentProfile.objects.create(
                user=user,
                course=self.cleaned_data['course'],
                student_id=student_id
            )
        return user



class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})

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