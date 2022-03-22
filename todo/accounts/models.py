from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(max_length=50)
    city = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
