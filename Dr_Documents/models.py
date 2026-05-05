from django.db import models
from django.contrib.auth.models import User
from Dr_personalInfo.models import DoctorPersonalInfo
from django.conf import settings


DOCUMENT_TYPE_CHOICES = (
    ('aadhaar', 'Aadhaar Card'),
    ('pan', 'PAN Card'),
    ('medical_license', 'Medical License'),
    ('medical_certificate', 'Medical Certificate'),
    ('experience_letter', 'Experience Letter'),
    ('other', 'Other'),
)


class DoctorDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)

    doctor = models.ForeignKey(
        DoctorPersonalInfo,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES
    )

    document_file = models.FileField(
        upload_to='doctor_documents/'
    )

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.user.username}"
