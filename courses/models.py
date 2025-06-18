from django.db import models
from users.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'FACULTY'})

class StudentEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'STUDENT'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)
