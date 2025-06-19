# urls.py
from django.urls import path
from . import views


app_name='courses'
urlpatterns = [
    path('courses-list/', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('courses/update/<int:pk>/', views.course_update, name='course_update'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
]
