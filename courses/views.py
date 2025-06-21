from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from .models import *
from materials.models import *  
from courses.models import *  
from django.contrib.auth.decorators import login_required

def is_admin(user):
    return user.is_authenticated and user.user_type == 'ADMIN'

@user_passes_test(is_admin)
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'Admin/course_list.html', {'courses': courses})

@user_passes_test(is_admin)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'Admin/course_create.html', {'form': form, 'title': 'Create Course'})

@user_passes_test(is_admin)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('courses:course_list')
    return render(request, 'Admin/course_create.html', {'form': form, 'title': 'Update Course'})

@user_passes_test(is_admin)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:course_list')
    return render(request, 'Admin/course_confirm_delete.html', {'course': course})




