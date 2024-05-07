from django.db import models

# Create your models here.

class Course(models.Model):
    section_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    timing = models.TimeField()
    faculty_name = models.CharField(max_length=100)  # Added field for faculty name

    def __str__(self):
        return f"Section {self.section_number}: {self.name} (Faculty: {self.faculty_name})"

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)
    courses = models.ManyToManyField(Course, through='StudentCourse')

    def __str__(self):
        return self.name

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} - Section {self.course.section_number}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    # present = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student.name} - Section {self.course.section_number} - {self.date.strftime('%Y-%m-%d')}"
