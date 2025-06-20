from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from courses.models import Course
from users.models import StudentProfile
from .models import Attendance

@login_required
def mark_attendance(request):
    faculty = request.user

    try:
        course = Course.objects.get(faculty=faculty)
    except Course.DoesNotExist:
        return render(request, 'students/mark_attendance.html', {
            'error': 'No course assigned to you.'
        })

    student_profiles = StudentProfile.objects.select_related('user').filter(course=course)
    today = timezone.now().date()

    if request.method == 'POST':
        for profile in student_profiles:
            user = profile.user
            key = f'present_{user.id}'
            status = "Present" if key in request.POST else "Absent"
            Attendance.objects.update_or_create(
                student=user,
                course=course,
                date=today,
                defaults={'status': status}
            )
        return redirect('mark-attendance')  # Ensure your URL name is correct

    marked_students = Attendance.objects.filter(course=course, date=today).values_list('student_id', flat=True)

    # Calculate total number of working days for course
    total_days = Attendance.objects.filter(course=course).values('date').distinct().count()

    # Calculate present days and percentage per student
    student_stats = {}
    for profile in student_profiles:
        user = profile.user
        present_days = Attendance.objects.filter(student=user, course=course, status='Present').count()
        percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0.0
        student_stats[user.id] = {
            'present_days': present_days,
            'total_days': total_days,
            'percentage': percentage,
        }

    return render(request, 'students/mark_attendance.html', {
        'course': course,
        'students': student_profiles,
        'today': today,
        'marked_students': list(marked_students),
        'student_stats': student_stats,
    })





@login_required
def student_attendance_view(request):
    user = request.user
    if user.user_type != 'STUDENT':
        return render(request, 'students/student_attendance.html', {
            'error': 'You are not authorized to view this page.'
        })

    attendance_records = Attendance.objects.filter(student=user).order_by('date')

    total_days = attendance_records.values('date').distinct().count()
    present_days = attendance_records.filter(status='Present').count()
    percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0

    return render(request, 'students/student_attendance.html', {
        'attendance_records': attendance_records,
        'total_days': total_days,
        'present_days': present_days,
        'percentage': percentage,
    })