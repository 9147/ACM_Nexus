from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from .models import *
import random
from django.core.mail import send_mail
from ACM_Registration_Portal.settings import EMAIL_HOST_USER
import random
import string

def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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
        USN=request.POST['USN']
        name=request.POST['name']
        year=request.POST['year']
        print(email,USN,name,year)
        password = generate_random_password(6)
        if CustomUser.objects.filter(email=email).exists():
            val=CustomUser.objects.get(email=email)
            val.set_password(password)
        else:
            print("he must login")
            val=CustomUser(email=email,USN=USN,first_name=name,year=year)
            val.set_password(password)
        send_mail(
            'Credentials for ACM Nexus',
            "Your username is "+email+"\n"+'Your password is '+password,
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        val.save()
        return render(request,'MainApp/confirmation.html')
    return HttpResponse(status=404)

def about(request):
    return render(request,'MainApp/about.html')

def account(request):
    return render(request,'MainApp/account.html')

def updatePassword(request,id):
    if request.method=='POST':
        user = CustomUser.objects.get(id=id)
        # print(user)
        # print(request.POST['password'])
        user.set_password(request.POST.get('password'))
        user.save()
        return HttpResponseRedirect('/account')
    return HttpResponse(status=404)

def recovery(request):
    return render(request,'MainApp/recovery.html')

def sendpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            user=CustomUser.objects.get(email=email)
            password=generate_random_password(6)
            user.set_password(password)
            send_mail(
                'Credentials for ACM Nexus',
                "Your username is "+email+"\n"+'Your password is '+password,
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            user.save()
            return render(request,'MainApp/confirmation.html')
        return render(request,'MainApp/confirmation.html')
    return HttpResponse(status=404)

def registration(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif Team.objects.filter(team_leader=request.user).exists():
        return render(request,'MainApp/registered.html',context={'team':Team.objects.get(team_leader=request.user)})
    elif Team.objects.filter(team_member1=request.user).exists():
        return render(request,'MainApp/registered.html',context={'team':Team.objects.get(team_member1=request.user)})
    elif Team.objects.filter(team_member2=request.user).exists():
        return render(request,'MainApp/registered.html',context={'team':Team.objects.get(team_member2=request.user)})
    elif Team.objects.filter(team_member3=request.user).exists():
        return render(request,'MainApp/registered.html',context={'team':Team.objects.get(team_member3=request.user)})
    return render(request,'MainApp/registration.html')

def createteam(request):
    if request.method=='POST':
        team_name=request.POST['name']
        team_leader=request.POST['email1']
        team_member1=request.POST['email2']
        team_member2=request.POST['email3']
        team_member3=request.POST['email4']
        if Team.objects.filter(team_name=team_name).exists():
            return HttpResponse(status=404)
        else:
            val=Team(team_name=team_name,team_leader=CustomUser.objects.get(email=team_leader),team_member1=CustomUser.objects.get(email=team_member1),team_member2=CustomUser.objects.get(email=team_member2),team_member3=CustomUser.objects.get(email=team_member3))
            val.save()
            return render(request,'MainApp/registered.html')
    return HttpResponse(status=404)

def checkteam(request):
    if request.method=='POST':
        team_name=request.POST['name']
        team_member1 = request.POST['email2']
        team_member2 = request.POST['email3']
        team_member3 = request.POST['email4']
        print(team_name,team_member1,team_member2,team_member3)
        print(CustomUser.objects.filter(email=team_member1))
        if Team.objects.filter(team_name=team_name).exists():
            return HttpResponse(status=404,reason='Team Name already exists\n Try with different name')
        elif not CustomUser.objects.filter(email=team_member1).exists():
            return HttpResponse(status=404,reason='Team Member 2 doesn\'t exists')
        elif not CustomUser.objects.filter(email=team_member2).exists():
            return HttpResponse(status=404,reason='Team Member 3 doesn\'t exists')
        elif not CustomUser.objects.filter(email=team_member3).exists():
            return HttpResponse(status=404,reason='Team Member 4 doesn\'t exists')
        elif Team.objects.filter(team_member1=CustomUser.objects.get(email=team_member1)).exists():
            return HttpResponse(status=404,reason='Team Member 2 already has team')
        elif Team.objects.filter(team_member2=CustomUser.objects.get(email=team_member2)).exists():
            return HttpResponse(status=404,reason='Team Member 3 already has team')
        elif Team.objects.filter(team_member3=CustomUser.objects.get(email=team_member3)).exists():
            return HttpResponse(status=404,reason='Team Member 4 already has team')
        else:
            return JsonResponse({'data':'success'})
    return HttpResponse(status=404)

def deleteteam(request,team_name):
    if request.method=='POST':
        team=Team.objects.get(team_name=team_name)
        team.delete()
        return HttpResponseRedirect('/account')
    return HttpResponse(status=404)
