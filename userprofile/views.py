from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course
from userprofile.models import *
# Create your views here.
@login_required(login_url='login')
def userProfilePage(request):
    # Access the username from the request.user object
    username = request.user.username
    courses = Course.objects.filter(faculty_name=username)
    # Pass the username to the template context
    context = {
        'username': username,
        'courses': courses
    }
    return render(request, 'profile.html',context)

def seeRecords(request, course_name, section_number):
    # Get the course object based on the provided name and section_number
    course = Course.objects.get(name=course_name, section_number=section_number)
    
    # Query attendance records for the specified course
    attendance_records = Attendance.objects.filter(course=course)
    
    # Initialize a dictionary to store student attendance counts
    student_attendance_counts = {}
    
    # Iterate over the attendance records to count attendance for each student
    for record in attendance_records:
        student_name = record.student.name
        student_id = record.student.student_id
        if student_name not in student_attendance_counts:
            student_attendance_counts[student_name] = {'id': student_id, 'count': 1}
        else:
            student_attendance_counts[student_name]['count'] += 1
    
    # Pass the attendance counts to the template
    context = {
        'course': course,
        'student_attendance_counts': student_attendance_counts
    }
    return render(request, 'seeRecords.html', context)
