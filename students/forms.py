# from django import forms
# from users.models import StudentProfile

# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = ['course', 'profile_picture', 'resume', 'aadhar_number',
#                   'father_name', 'mother_name', 'enrollment_date',
#                   'qualification', 'placement_company']
        


from django import forms
from users.models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [ 'course', 'profile_picture', 'resume',
            'aadhar_number', 'father_name', 'mother_name',
            'enrollment_date', 'qualification', 'placement_company']
        
           
        
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)

        # Read-only course field
        course_name = self.instance.course.name if self.instance and self.instance.course else ''
        self.fields['course'] = forms.CharField(
            label='Course',
            initial=course_name,
            required=False,
            widget=forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control bg-light',
            })
        )

        # Read-only user field (e.g., show user's full name or email)
        user_display = self.instance.user.get_full_name() if self.instance and self.instance.user else ''
        self.fields['user'] = forms.CharField(
            label='User',
            initial=user_display,
            required=False,
            widget=forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control bg-light',
            })
        )

        # Style other fields
        for name, field in self.fields.items():
            if name in ['profile_picture', 'resume']:
                field.widget.attrs['class'] = 'form-control-file'
            elif name not in ['course', 'user']:
                field.widget.attrs['class'] = 'form-control'

    # Prevent saving invalid data for course
    def clean_course(self):
        return self.instance.course

    # Prevent saving invalid data for user
    def clean_user(self):
        return self.instance.user
