from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    USN = models.CharField(max_length=10, unique=True)
    OTP = models.CharField(max_length=6, unique=True,default='000000')
    USERNAME_FIELD = "email"
    year=models.CharField(max_length=4,default='2025')
    verified=models.BooleanField(default=False)
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
