from django.db import models
from django.conf import settings

class Doctor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PastMedication(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="past_medications")

    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)

    prescribing_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication_name} - {self.patient.username}"