from django.urls import path

# Your URL patterns

from . import views

urlpatterns=[
    path('', views.dbmanage, name='dbmanage'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_student/', views.add_student, name='add_student'),
    path('assign_student_to_course/', views.assign_student_to_course, name='assign_student_to_course'),
    path('students/', views.student_list, name='student_list'),
    path('courses/', views.course_list, name='course_list'),
    path('student-courses/', views.student_course_list, name='student_course_list'),
]