# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

#------------ADDRESS


class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

class Profile(models.Model):
    POST_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    post = models.CharField(max_length=10, choices=POST_CHOICES)
    language = models.CharField(max_length=50)
    google_connected = models.BooleanField(default=False)
    google_email = models.EmailField(null=True, blank=True)
#doctor class


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    specialty = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()  # years
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#user class 


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('DOCTOR', 'DOCTOR'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    # Fix clashes with default auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


# Example UserProfile pointing to custom User


class UserProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts_userprofile_set'  # <--- add unique related_name
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

