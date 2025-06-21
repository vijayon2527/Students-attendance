
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from users.models import *
from .forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
from courses.models import Course
from materials.models import *
from .models import *  



@login_required
def student_profile_view(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('students:studentprofile_list')  
    else:
        form = StudentProfileForm(instance=student_profile)

    return render(request, 'students/studentprofile_list.html', {
        'student_profile': student_profile,
        'form': form
    })


@login_required
def student_materials_view(request):
    if request.user.user_type != 'STUDENT':
        return redirect('users:home')

    try:
        profile = request.user.studentprofile
        student_course = profile.course
        materials = CourseMaterial.objects.filter(course=student_course).order_by('-uploaded_at')
    except StudentProfile.DoesNotExist:
        materials = []

    return render(request, 'students/student_materials.html', {'materials': materials})


def is_admin_or_faculty(user):
    return user.is_authenticated and user.user_type in ['ADMIN', 'FACULTY']


@login_required
@user_passes_test(is_admin_or_faculty)
def manage_timetable(request):
    entries = TimetableEntry.objects.all()
    form = TimetableEntryForm()
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_timetable')
    return render(request, 'admin/edit_timetable.html', {'form': form, 'entries': entries})


@login_required
@user_passes_test(is_admin_or_faculty)
def manage_events(request):
    events = CourseEvent.objects.all()
    form = CourseEventForm()
    if request.method == 'POST':
        form = CourseEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students:event_list')
    return render(request, 'Admin/manage_events.html', {'form': form, 'events': events})


@login_required
@user_passes_test(is_admin_or_faculty)
def event_list(request):
    events = CourseEvent.objects.all().order_by('-date')
    return render(request, 'Admin/event_list.html', {'events': events})


@login_required
@user_passes_test(is_admin_or_faculty)
def event_edit(request, event_id):
    event = get_object_or_404(CourseEvent, id=event_id)
    form = CourseEventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('students:event_list')
    return render(request, 'Admin/event_edit.html', {'form': form, 'event': event})


@login_required
@user_passes_test(is_admin_or_faculty)
def delete_event(request, event_id):
    event = get_object_or_404(CourseEvent, id=event_id)
    course_id = event.course.id
    event.delete()
    return redirect('manage_events', course_id=course_id)


DAY_ORDER = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


@login_required
def student_schedule(request):
    profile = request.user.studentprofile
    course = profile.course

    # Fetch and manually sort timetable by day order and start time
    timetable = TimetableEntry.objects.filter(course=course)
    timetable = sorted(timetable, key=lambda x: (DAY_ORDER.get(x.day, 99), x.start_time))

    events = CourseEvent.objects.filter(course=course).order_by('date', 'time')

    return render(request, 'students/student_schedule.html', {
        'course': course,
        'timetable': timetable,
        'events': events
    })


def admin_course_list(request):
    courses = Course.objects.all()
    return render(request, 'Admin/admin_course_list.html', {'courses': courses})


def admin_course_timetable(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    timetable = TimetableEntry.objects.filter(course=course)
    students = StudentProfile.objects.filter(course=course)
    return render(request, 'Admin/course_timetable.html', {
        'course': course,
        'timetable': timetable,
        'students': students
    })


def create_timetable_entry(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.course = course  # Associate course automatically
            timetable.save()
            return redirect('students:admin_course_timetable', course_id=course.id)
    else:
        form = TimetableEntryForm(initial={'course': course})

    return render(request, 'Admin/create_timetable.html', {
        'form': form,
        'course': course
    })


def edit_timetable_entry(request, entry_id):
    entry = get_object_or_404(TimetableEntry, id=entry_id)
    
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('students:admin_course_timetable', course_id=entry.course.id)  # Adjust this name if needed
    else:
        form = TimetableEntryForm(instance=entry)

    return render(request, 'Admin/edit_timetable.html', {
        'form': form,
        'entry': entry,
    })


class StudentsByCourseView(ListView):
    model = StudentProfile
    template_name = 'Admin/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        course_id = self.request.GET.get('course_id')
        if course_id:
            return StudentProfile.objects.filter(course_id=course_id)
        return StudentProfile.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context