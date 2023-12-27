from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login,logout
from .models import *
import random
from django.core.mail import send_mail
from ACM_Registration_Portal.settings import EMAIL_HOST_USER
# Create your views here.
def home(request):
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     EMAIL_HOST_USER,
    #     ['shubhammirashi303@gmail.com'],
    #     fail_silently=False,
    # )
    return render(request,'MainApp/home.html')

def loginPage(request):
    return render(request,'MainApp/login.html')

def event(request):
    return render(request,'MainApp/event.html')

def logoutPage(request):
    logout(request)
    return home(request)

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            print("success")
            return JsonResponse({'data':'success'})
        else:
            return HttpResponse(status=401)
    return HttpResponse(status=404)

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        USN=request.POST['USN']
        name=request.POST['name']
        year=request.POST['year']
        print(email,password,USN,name,year)
        otp=""
        for i in range(4):
            otp += str(random.randint(1, 9))
        if CustomUser.objects.filter(email=email).exists():
            if CustomUser.objects.filter(email=email,verified=False).exists():
                val=CustomUser.objects.get(email=email)
                val.delete()
            else:
                print("he must login")
                return HttpResponse("email")
        val=CustomUser(email=email,password=password,USN=USN,first_name=name,year=year,OTP=otp)
        login(request,val)
        val.save()
    return HttpResponse("hello")

def about(request):
    return render(request,'MainApp/about.html')