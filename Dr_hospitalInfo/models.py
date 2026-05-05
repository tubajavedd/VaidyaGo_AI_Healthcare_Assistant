from django.db import models
from Dr_personalInfo.models import DoctorPersonalInfo


EMPLOYMENT_TYPE_CHOICES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('visiting', 'Visiting'),
)


class DoctorHospitalInfo(models.Model):

    doctor = models.OneToOneField(
        DoctorPersonalInfo,
        on_delete=models.CASCADE,
        related_name='hospital_info'
    )

    joining_date = models.DateField()
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES
    )

    consultation_fees = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    leave_day = models.CharField(
        max_length=20,
        help_text="e.g. Sunday or Monday"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hospital Info for Doctor {self.doctor.id}"
