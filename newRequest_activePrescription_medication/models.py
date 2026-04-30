from django.db import models
from django.conf import settings

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50, default="10mg")

    def __str__(self):
        return f"{self.name} {self.dosage}"


class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class PrescriptionRequest(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Home Delivery'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)