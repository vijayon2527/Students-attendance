from django.urls import path
from .views import *

app_name='students'

urlpatterns = [
    path('students/', student_profile_view, name='studentprofile_list'),
    path('students/by_courses/', StudentsByCourseView.as_view(), name='student_courses'),

    path('student/', student_materials_view, name='student_materials'),

    path('student/schedule/', student_schedule, name='student_schedule'),
    path('admin/timetable/', manage_timetable, name='manage_timetable'),
    path('admin/events/', manage_events, name='manage_events'),
    path('events/', event_list, name='event_list'),
    path('events/edit/<int:event_id>/', event_edit, name='event_edit'),
     path('events/delete/<int:event_id>/',delete_event, name='delete_event'),

    path('admin/courses/',admin_course_list, name='admin_course_list'),
    path('admin/courses/<int:course_id>/timetable/',admin_course_timetable, name='admin_course_timetable'),


    path('create-timetable/<int:course_id>/',create_timetable_entry, name='timetable_create'),
    path('admin/timetable/edit/<int:entry_id>/', edit_timetable_entry, name='timetable_edit'),

]
