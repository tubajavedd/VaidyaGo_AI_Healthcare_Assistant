# adminProfile/models.py
from django.db import models
from django.conf import settings

class Address(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_address'  # <-- add unique related_name
    )
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

class Profile(models.Model):
    POST_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile'  # <-- add unique related_name
    )
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    post = models.CharField(max_length=10, choices=POST_CHOICES)
    language = models.CharField(max_length=50)
    google_connected = models.BooleanField(default=False)
    google_email = models.EmailField(null=True, blank=True)
