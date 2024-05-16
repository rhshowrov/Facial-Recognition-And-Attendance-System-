from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint
from datetime import datetime

from django.db import models

class Course(models.Model):
    section_number = models.IntegerField()
    name = models.CharField(max_length=100)
    timing = models.CharField(max_length=20)  # Change to CharField to store the time in '12:15 PM' format
    faculty_name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['section_number', 'name'], name='unique_section_per_course')
        ]

    def __str__(self):
        return f"Section {self.section_number}: {self.name} (Faculty: {self.faculty_name})"
    
    def formatted_timing(self):
        return self.timing  # You can still have the formatted_timing method if needed
    
    def save(self, *args, **kwargs):
        # Parse the input string to a time object
        try:
            time_obj = datetime.strptime(self.timing, '%I:%M %p').time()
            # Convert the time object back to a string in the desired format
            self.timing = time_obj.strftime('%I:%M %p')
        except ValueError:
            raise ValueError('Enter a valid time in HH:MM AM/PM format.')

        super().save(*args, **kwargs)

# class Course(models.Model):
#     section_number = models.IntegerField(unique=True)
#     name = models.CharField(max_length=100)
#     timing = models.TimeField()
#     faculty_name = models.CharField(max_length=100)  # Added field for faculty name

#     def __str__(self):
#         return f"Section {self.section_number}: {self.name} (Faculty: {self.faculty_name})"

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
