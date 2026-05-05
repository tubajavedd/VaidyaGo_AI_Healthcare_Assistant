from django.db import models
from django.conf import settings
from TodaySchedule_medication.models import Schedule
from newRequest_activePrescription_medication.models import PrescriptionRequest




class AccountSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="AccountSettings"
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    clinician_id = models.CharField(max_length=100, unique=True)

    language = models.CharField(
        max_length=100,
        default="English (United Kingdom)"
    )
    timezone = models.CharField(
        max_length=100,
        default="GMT +05:30 (Mumbai, India)"
    )
    automatic_updates = models.BooleanField(default=True)

    two_factor_enabled = models.BooleanField(default=False)

    data_sharing = models.BooleanField(default=False)

    profile_visibility = models.CharField(
        max_length=50,
        default="internal_only"
    )

    hipaa_logs_enabled = models.BooleanField(default=True)

    account_deactivated = models.BooleanField(default=False)
    request_data_deletion = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class UpdateLog(models.Model):
    STATUS_CHOICES=[
        ("taken_with_food","Taken with food"),
        ("taken_solo","Taken solo"),
        ("taken","Taken"),
        ("missed","Missed"),
        ("delyed","Delayed"),
        ("yesterday","Yesterday"),
        ("other","Other"),
   ]
        
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="update_log"
    )

    today_schedule =models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name="logs"
    )
    prescription=models.ForeignKey(
        PrescriptionRequest,
        on_delete=models.CASCADE,
        related_name="logs"

    )


    status = models.CharField(
            max_length=30,
            choices = STATUS_CHOICES
    )

    clinical_observation = models.TextField(
        blank=True,
        null=True
    )

    symptoms= models.JSONField(
        default=list,
        blank=True
    )
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}-{self.status}"

