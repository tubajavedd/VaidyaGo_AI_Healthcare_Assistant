# reminders/models.py
from django.db import models
from django.conf import settings


class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)

    frequency = models.CharField(max_length=50)
    duration_days = models.IntegerField()

    times = models.JSONField()

    start_date = models.DateField()
    end_date = models.DateField()

    next_trigger = models.DateTimeField()

    status = models.CharField(max_length=20, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
