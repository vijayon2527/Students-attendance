from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *




def home_view(request):
    return render(request, 'pages/Home.html')

def about_view(request):
    return render(request, 'pages/About.html')

def contact_view(request):
    return render(request, 'pages/Contact.html')


def courses_view(request):
    return render(request, 'pages/Courses.html')



@login_required
def admin_dashboard(request):
    return render(request, 'Dashboards/admin_dashboard.html')


def faculty_dashboard(request):
    faculty_user = request.user  
    course = Course.objects.filter(faculty=faculty_user).first()
    students = StudentProfile.objects.filter(course=course)

    return render(request, "Dashboards/faculty_dashboard.html", {
        "course": course,
        "students": students,
    })

@login_required
def student_dashboard(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'Dashboards/student_dashboard.html', {
        'user': request.user,
        'student_profile': student_profile
    })


@login_required
def faculty_students(request):
    faculty_user = request.user  # must have user_type='FACULTY'
    course = Course.objects.filter(faculty=faculty_user).first()
    students = StudentProfile.objects.filter(course=course) if course else []

    return render(request, "students/faculty_students.html", {
        "course": course,
        "students": students
    })


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect to appropriate dashboard
            if user.user_type == 'ADMIN':
                return redirect('users:admin_dashboard')
            elif user.user_type == 'FACULTY':
                return redirect('users:faculty_dashboard')
            elif user.user_type == 'STUDENT':
                return redirect('users:student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:home')


@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'Admin/users_list.html', {'users': users})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:users_list')
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, 'Admin/update_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('users:users_list')