from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, FacultyProfile
from django.contrib.auth.forms import UserChangeForm
from courses.models import Course



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile
from courses.models import Course

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=15)
    # Removed user_type field — it will be set in save()
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', "user_type",'email', 'phone_number', 'password1', 'password2', 'course', 'profile_picture']

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if not course:
            raise forms.ValidationError("Please select a valid course.")
        return course

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'STUDENT'  # Force user type to STUDENT
        user.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                course=self.cleaned_data.get('course'),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user


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