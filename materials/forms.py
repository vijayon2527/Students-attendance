from django import forms
from .models import CourseMaterial


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        exclude = ['uploaded_by', 'course', 'uploaded_at']

