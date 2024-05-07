from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def basePage(request):
    return render(request,'base.html')


def signupPage(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if(password1!=password2):
            return HttpResponse("passwords are not matching")
        else:
            my_user=User.objects.create_user(uname,email,password1)
            my_user.save()
            return redirect('login')
        
        #print(uname,email,password1,password2)
    return render(request,'signup.html')


def loginPage(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        password=request.POST.get('pass')
        user=authenticate(request,username=uname,password=password)
        if user is not None:
            login(request,user)
            return redirect('base')
        else:
            return HttpResponse("invalid credentials")
    return render(request,'login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')