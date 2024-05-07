from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course
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