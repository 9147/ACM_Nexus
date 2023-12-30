from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from .models import *
import random
from django.core.mail import send_mail
from ACM_Registration_Portal.settings import EMAIL_HOST_USER
import random
import string
from django.conf import settings
import os
import csv

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
        if Team.objects.filter(team_name=team_name).exists():
            return HttpResponse(status=404)
        else:
            return render(request,'MainApp/registration.html')
    return HttpResponse(status=404)

def checkteam(request):
    if request.method=='POST':
        team_name=request.POST['name']
        team_leader=request.POST['email1']
        team_member1 = request.POST['email2']
        team_member2 = request.POST['email3']
        team_member3 = request.POST['email4']
        problem_number=request.POST.get('problem')
        print(team_name,team_member1,team_member2,team_member3)
        print(CustomUser.objects.filter(email=team_member1))
        if Team.objects.filter(team_name=team_name).exists():
            return HttpResponse(status=404,reason='Team Name already exists\n Try with different name')
        elif problem_number not in [str(i) for i in range(1,26)]:
            return HttpResponse(status=404,reason='Problem Number is not valid')
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
            u1 = CustomUser.objects.get(email=team_leader)
            u1.is_registered = True
            u2 = CustomUser.objects.get(email=team_member1)
            u2.is_registered = True
            u3 = CustomUser.objects.get(email=team_member2)
            u3.is_registered = True
            u4 = CustomUser.objects.get(email=team_member3)
            u4.is_registered = True
            val = Team(team_name=team_name, team_leader=u1, team_member1=u2, team_member2=u3, team_member3=u4,
                       problem_no=problem_number)
            val.save()
            u1.save()
            u2.save()
            u3.save()
            u4.save()
            return JsonResponse({'data':'success'})
    return HttpResponse(status=404)

def deleteteam(request,team_name):
    if request.method=='POST':
        team=Team.objects.get(team_name=team_name)
        u1 = team.team_leader
        u2 = team.team_member1
        u3 = team.team_member2
        u4 = team.team_member3
        u1.is_registered=False
        u2.is_registered=False
        u3.is_registered=False
        u4.is_registered=False
        u1.save()
        u2.save()
        u3.save()
        u4.save()
        team.delete()
        return HttpResponseRedirect('/account')
    return HttpResponse(status=404)


def problems(request):
    f = open(os.path.join(settings.STATIC_ROOT, 'data/data.csv'), 'r')
    reader = csv.reader(f)
    next(reader)
    data_list = list(reader)

    s = {}
    theme = {}
    no = 1
    count = 1
    val = "Sustainability and Environment"

    for a in data_list:
        if val == a[1]:
            if count not in s:
                s[count] = []
            s[count].append((no, a[0]))
            no += 1
        else:
            theme[count] = val
            count += 1
            val = a[1]

            if count not in s:
                s[count] = []
            s[count].append((no, a[0]))
            no += 1

    theme[count] = val

    f.close()
    return render(request, 'MainApp/problems.html', context={'theme': theme.items(), 'data': s.items()})

def getteams(request):
    if request.user.is_superuser:
        f=open(os.path.join(settings.STATIC_ROOT,'data/teams.csv'),'w',newline='')
        writer=csv.writer(f)
        writer.writerow(['Team Name','Team Leader','Team Member 1','Team Member 2','Team Member 3','Problem Number'])
        for team in Team.objects.all():
            writer.writerow([team.team_name,team.team_leader.email,team.team_member1.email,team.team_member2.email,team.team_member3.email,team.problem_no])
        f.close()
        return JsonResponse({'data':list(Team.objects.all().values())})
    return HttpResponse(status=404)