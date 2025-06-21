from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CourseMaterial
from courses.models import Course
from .forms import CourseMaterialForm
from users.models import User


@login_required
def upload_material(request):
    if request.user.user_type != 'FACULTY':
        return redirect('home')

    # Get course assigned to this faculty
    try:
        course = Course.objects.get(faculty=request.user)
    except Course.DoesNotExist:
        return render(request, 'students/materials_upload.html', {
            'form': None,
            'error': 'No course assigned to you.'
        })

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.course = course  # assign course automatically
            material.save()
            return redirect('materials:list')
    else:
        form = CourseMaterialForm()

    return render(request, 'students/materials_upload.html', {'form': form})

# List materials for students and faculty
@login_required
def material_list(request):
    if request.user.user_type == 'STUDENT':
        # Show only materials related to student's courses
        student_courses = request.user.student.course.all()
        materials = CourseMaterial.objects.filter(course__in=student_courses)
    elif request.user.user_type == 'FACULTY':
        # Show materials uploaded by faculty
        materials = CourseMaterial.objects.filter(uploaded_by=request.user)
    else:
        materials = CourseMaterial.objects.all()

    return render(request, 'students/material_list.html', {'materials': materials})
