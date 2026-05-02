from django.db import models
from django.conf import settings

class Medication(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#pharmacy
class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone=models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.name

class PrescriptionRequest(models.Model):
    DELIVERY_CHOICES = [
        ("pickup", "Pickup"),
        ("delivery", "Home Delivery"),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)

    delivery_preference = models.CharField(   # ✅ ADD THIS
        max_length=20,
        choices=DELIVERY_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)