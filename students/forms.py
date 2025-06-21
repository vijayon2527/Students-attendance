from django import forms
from users.models import *
from .models import *

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'course', 'profile_picture', 'resume',
            'aadhar_number', 'father_name', 'mother_name',
            'enrollment_date', 'qualification', 'placement_company'
        ]
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)

        # Apply white background and dark text to all fields
        for name, field in self.fields.items():
            if name in ['profile_picture', 'resume']:
                field.widget.attrs.update({
                    'class': 'form-control-file bg-dark text-white'
                })
            elif name == 'course':
                field.disabled = True
                field.widget.attrs.update({
                    'class': 'form-control bg-dark text-white'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control bg-dark text-white'
                })

    def clean_course(self):
        return self.instance.course

class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TimetableEntryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'color: white;'
            })



class CourseEventForm(forms.ModelForm):
    class Meta:
        model = CourseEvent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseEventForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'color: white;'
            })


