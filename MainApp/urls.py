from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'MainApp'

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('event/', event, name='event'),
    path('logout/',logoutPage,name='logoutPage'),
    path('signin/',signin,name='signin'),
    path('register/',register,name='register'),
    path('about/',about,name='about'),
]
