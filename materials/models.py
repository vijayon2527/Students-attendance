from django.db import models
from courses.models import Course
from users.models import User

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    material_type = models.CharField(max_length=20, choices=(('Syllabus', 'Syllabus'), ('PDF', 'PDF')))
