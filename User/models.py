from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('You must add email.'))

        user = self.model(
            email=self.normalize_email(email),
            name = name, 
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault("is_admin", True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address.'), unique=True)
    name = models.CharField(max_length=150, unique=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    about = models.CharField(max_length=300, blank=True)
    profile_img = models.ImageField(upload_to = "users/profiles/",blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name