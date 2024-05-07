"""
URL configuration for frasystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userlogin.views import loginPage,signupPage,basePage,logoutPage
from tkAtt.views import tkAtt
from userprofile.views import userProfilePage

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', admin.site.urls),\
    path('',signupPage,name='signup' ),
    path('login/',loginPage,name='login' ),
    path('base/',basePage,name='base' ),
    path('tkAtt//<str:course_name>/<int:section_number>/',tkAtt,name='tkAtt' ),
    path('logout/',logoutPage,name='logout' ),
    path('userprofile/',userProfilePage,name='userprofile' ),


]
