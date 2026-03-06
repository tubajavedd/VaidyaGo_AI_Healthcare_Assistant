from django.db import models

class DoctorSlot(models.Model):
    doctor = models.ForeignKey(
        "Dr_personalInfo.DoctorPersonalInfo",
        on_delete=models.CASCADE
    )
    from_date = models.DateField()
    to_date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    slot_duration = models.IntegerField()  # 10,15,20,30
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor} | {self.from_date} - {self.to_date}"
