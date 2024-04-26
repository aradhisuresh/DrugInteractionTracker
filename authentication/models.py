from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=30, default='Anonymous')
    email = models.EmailField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []