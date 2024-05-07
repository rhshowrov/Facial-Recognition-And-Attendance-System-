from django.contrib import admin
from .models import Course, Student,StudentCourse, Attendance
# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(StudentCourse)
admin.site.register(Attendance)