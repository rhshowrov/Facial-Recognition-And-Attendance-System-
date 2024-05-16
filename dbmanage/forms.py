
from django import forms
from userprofile.models import Course, Student, StudentCourse
from datetime import datetime

# forms.py


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['section_number', 'name', 'timing', 'faculty_name']
        widgets = {
            'section_number': forms.NumberInput(attrs={
                'class': 'block w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300'
            }),
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300'
            }),
            'timing': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'HH:MM AM/PM'
            }),
            'faculty_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300'
            }),
        }

    def clean_timing(self):
        timing = self.cleaned_data.get('timing').strip()  # Remove leading and trailing whitespaces
        try:
            # Parse the input string to a time object
            time_obj = datetime.strptime(timing, '%I:%M %p').time()
            # Convert the time object back to a string in the desired format
            formatted_timing = time_obj.strftime('%I:%M %p')
            return formatted_timing
        except ValueError:
            raise forms.ValidationError('Enter a valid time in HH:MM AM/PM format.')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id']
        labels = {
            'name': 'Student Name:',
            'student_id': 'Student ID:',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md border focus:outline-none focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Enter student name...',
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md border focus:outline-none focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Enter student ID...',
            }),
        }

class StudentCourseForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['student', 'course']
        labels = {
            'student': 'Student:',
            'course': 'Course:',
        }
        widgets = {
            'student': forms.Select(attrs={
                'class': 'w-full px-3 py-2 rounded-md border focus:outline-none focus:border-blue-500',
            }),
            'course': forms.Select(attrs={
                'class': 'w-full px-3 py-2 rounded-md border focus:outline-none focus:border-blue-500',
            }),
        }
