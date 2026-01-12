# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('DOCTOR', 'DOCTOR'),
        ('PATIENT', 'PATIENT'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
