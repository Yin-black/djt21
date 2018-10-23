from django.db import models
from django.db.models import CharField,IntegerField,EmailField
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, telephone,username,password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        user = self.model(telephone = telephone,username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( telephone,username, password, **extra_fields)

    def create_superuser(self, username, telephone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(telephone,username, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    """
    重构User
    """
    telephone = CharField(max_length=11,unique=True)
    username = CharField(max_length=50)
    email = EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)
    join_data = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username','email']

    objects = UserManager()
