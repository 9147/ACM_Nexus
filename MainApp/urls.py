from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'MainApp'

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('event/', event, name='event'),
    path('logout/',logoutPage,name='logout'),
    path('signin/',signin,name='signin'),
    path('register/',register,name='register'),
    path('about/',about,name='about'),
    path('account/',account,name='account'),
    path('account/updatePassword/<int:id>',updatePassword,name='updatePassword'),
    path('recovery/',recovery,name='recovery'),
    path('sendpassword/',sendpassword,name='sendpassword'),
    path('registration/',registration,name='registration'),
    path('createteam/',createteam,name='createteam'),
    path('checkteam/',checkteam,name='checkteam'),
    path('deleteteam/<str:team_name>',deleteteam,name='deleteteam'),
    path('problems/',problems,name='problems'),
    path('getteams/',getteams,name='getteams'),
]
