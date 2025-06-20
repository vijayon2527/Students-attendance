from django.db import models
from users.models import User
from courses.models import Course

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'STUDENT'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

    
    class Meta:
        unique_together = ('student', 'course', 'date')  # avoid duplicate attendance for same day

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.date} - {self.status}"