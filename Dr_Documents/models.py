from django.db import models
from Dr_personalInfo.models import DoctorPersonalInfo


DOCUMENT_TYPE_CHOICES = (
    ('aadhaar', 'Aadhaar Card'),
    ('pan', 'PAN Card'),
    ('medical_license', 'Medical License'),
    ('medical_certificate', 'Medical Certificate'),
    ('experience_letter', 'Experience Letter'),
    ('other', 'Other'),
)


class DoctorDocument(models.Model):

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

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for Doctor {self.doctor.id}"
