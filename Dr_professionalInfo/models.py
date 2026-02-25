from django.db import models
from Dr_personalInfo.models import DoctorPersonalInfo


class DoctorProfessionalInfo(models.Model):

    doctor = models.OneToOneField(
        DoctorPersonalInfo,
        on_delete=models.CASCADE,
        related_name='professional_info'
    )

    doctor_employee_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    years_of_experience = models.PositiveIntegerField()
    medical_license_number = models.CharField(max_length=100)
    medical_council = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Professional Info for Doctor {self.doctor.id}"
