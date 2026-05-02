from django.db import models
from django.conf import settings

class Medication(models.Model):
    name = models.CharField(max_length=100)
<<<<<<< HEAD

    def __str__(self):
        return self.name

#pharmacy
class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone=models.CharField(max_length=20,null=True, blank=True)
=======
    dosage = models.CharField(max_length=50, default="10mg")

    def __str__(self):
        return f"{self.name} {self.dosage}"


class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff

    def __str__(self):
        return self.name

<<<<<<< HEAD
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

=======

class PrescriptionRequest(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Home Delivery'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
    created_at = models.DateTimeField(auto_now_add=True)