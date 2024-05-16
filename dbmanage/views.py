# views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from userprofile.models import Course, Student, StudentCourse
from .forms import CourseForm, StudentForm, StudentCourseForm


def dbmanage(request):
    if not request.user.is_superuser:
        return render(request, '403.html')
    else:
        return render(request, 'dbmanage.html')
    
# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CourseForm
from django.db import IntegrityError

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Course added successfully.')
                return redirect('add_course')
            except IntegrityError:
                form.add_error(None, 'A course with this section number and name already exists.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})


def add_student(request):
    if not request.user.is_superuser:
        return render(request, '403.html') 
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')  # Assuming you have a view to list students
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def assign_student_to_course(request):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student assigned to course successfully.')
            return redirect('assign_student_to_course')  # Assuming you have a view to list student-course assignments
    else:
        form = StudentCourseForm()
    return render(request, 'assign_student_to_course.html', {'form': form})


# View to display the list of students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# View to display the list of courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# View to display which students are assigned to which courses
def student_course_list(request):
    student_courses = StudentCourse.objects.select_related('student', 'course').all()
    return render(request, 'student_course_list.html', {'student_courses': student_courses})

