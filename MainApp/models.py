from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    USN = models.CharField(max_length=10)
    USERNAME_FIELD = "email"
    is_registered=models.BooleanField(default=False)
    year=models.CharField(max_length=4,default='2025')
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Team(models.Model):
    team_name=models.CharField(max_length=100,primary_key=True)
    team_leader=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    team_member1=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='team_member1',null=True,blank=True)
    team_member2=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='team_member2',null=True,blank=True)
    team_member3=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='team_member3',null=True,blank=True)
    problem_no=models.IntegerField(default=1,validators=[MaxValueValidator(25), MinValueValidator(1)])
    def __str__(self):
        return self.team_name
