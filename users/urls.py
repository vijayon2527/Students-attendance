from django.urls import path
from .views import *

app_name='users'
urlpatterns = [
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', faculty_dashboard, name='faculty_dashboard'),
    path('',home_view, name='home'),
    path('about/',about_view, name='about'),
    path('courses/',courses_view, name='courses'),
    path('contact/',contact_view, name='contact'),
   
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('users-list/', users_list, name='users_list'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),

     path('faculty/students/', faculty_students, name='faculty_students'),
]
