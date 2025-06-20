from django.urls import path
from .views import (
    StudentProfileListView,
    StudentProfileCreateView,
    StudentProfileDetailView,
    StudentProfileUpdateView,
    StudentProfileDeleteView,  
    StudentsByCourseView,
    student_profile_view
)

app_name='students'

urlpatterns = [
    path('students/', student_profile_view, name='studentprofile_list'),
    path('students/create/', StudentProfileCreateView.as_view(), name='studentprofile_create'),
    path('students/<int:pk>/', StudentProfileDetailView.as_view(), name='studentprofile_detail'),
    path('students/<int:pk>/edit/', StudentProfileUpdateView.as_view(), name='studentprofile_update'),
    path('students/<int:pk>/delete/', StudentProfileDeleteView.as_view(), name='studentprofile_delete'),  
    path('students/by_courses/', StudentsByCourseView.as_view(), name='student_courses'),
]
