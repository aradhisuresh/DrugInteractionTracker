from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import BaseUserManager

    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField('auth.Group', verbose_name='groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name='user permissions', blank=True, related_name='custom_user_permissions')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.username

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.token