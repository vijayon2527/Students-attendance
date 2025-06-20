from django.db import models
from users.models import User
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'FACULTY'}
    )

    def __str__(self):
        return self.name

class StudentEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'STUDENT'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)
