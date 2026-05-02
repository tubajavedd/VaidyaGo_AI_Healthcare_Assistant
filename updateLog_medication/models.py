from django.db import models
from django.conf import settings
from TodaySchedule_medication.models import Schedule
from newRequest_activePrescription_medication.models import PrescriptionRequest

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

