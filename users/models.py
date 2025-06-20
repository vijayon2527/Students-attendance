from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FACULTY', 'Faculty'),
        ('STUDENT', 'Student'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)

    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True) 
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    resume = models.FileField(upload_to='student_resumes/', blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)

    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)

    enrollment_date = models.DateTimeField(default=timezone.now)
    qualification = models.CharField(max_length=100, blank=True, null=True)

    is_placed = models.BooleanField(default=False)
    placement_company = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='faculty_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
 