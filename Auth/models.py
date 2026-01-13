# Auth/models.py
from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_userprofile_set'  # <--- add unique related_name
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
