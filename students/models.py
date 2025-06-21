# models.py

from django.db import models
from django.conf import settings
from courses.models import Course

class TimetableEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])
    subject = models.CharField(max_length=100)  # e.g., Python, Soft Skills
    start_time = models.TimeField()
    end_time = models.TimeField()
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'user_type': 'FACULTY'})

    def __str__(self):
        return f"{self.course.name} - {self.subject} on {self.day}"

# Extra events like mock tests/interviews
class CourseEvent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    event_type = models.CharField(max_length=100, choices=[
        ('Mock Test', 'Mock Test'),
        ('Interview', 'Interview'),
        ('Workshop', 'Workshop'),
        ('Announcement', 'Announcement'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.name}"
