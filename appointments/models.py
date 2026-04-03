from django.db import models
from Dr_personalInfo.models import DoctorPersonalInfo
from DoctorSlot.models import TimeSlot

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]

    # Doctor (already exists)
    doctor = models.ForeignKey(
        DoctorPersonalInfo,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    slot = models.ForeignKey(
    TimeSlot,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )
    
    # FUTURE USER (optional for now)
    user = models.IntegerField(null=True, blank=True)
    # 👉 Later replace with ForeignKey

    # Patient details (for now)
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=15)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor}"

    # ✅ conflict check
    def save(self, *args, **kwargs):
        conflict = Appointment.objects.filter(
            doctor=self.doctor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status='booked'
        ).exclude(id=self.id).exists()

        if conflict:
            raise ValueError("Slot already booked")

        super().save(*args, **kwargs)