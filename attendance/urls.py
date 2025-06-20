from django.urls import path
from .views import *

urlpatterns = [
    path('mark-attendance/',mark_attendance,name='mark-attendance'),
     path('student/attendance/', student_attendance_view, name='student-attendance'),
]
