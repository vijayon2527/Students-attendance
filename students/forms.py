from django import forms
from users.models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['course', 'profile_picture', 'resume', 'aadhar_number',
                  'father_name', 'mother_name', 'enrollment_date',
                  'qualification', 'placement_company']
        

