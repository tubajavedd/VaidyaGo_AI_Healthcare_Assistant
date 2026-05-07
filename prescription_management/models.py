from django.db import models
from django.conf import settings
from datetime import date, timedelta
from django.utils import timezone

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions')
    image = models.ImageField(upload_to='prescriptions/', null=True, blank=True)
    file = models.FileField(upload_to='prescriptions/files/', null=True, blank=True)
    
    doctor_name = models.CharField(max_length=255, null=True, blank=True)
    hospital_name = models.CharField(max_length=255, null=True, blank=True)
    prescription_date = models.DateField(null=True, blank=True)
    extracted_patient_name = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=100, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    findings = models.JSONField(default=list, blank=True)
    test_results = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    special_instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self):
        if self.status == 'completed':
            return
        
        has_active_meds = False
        p_date = self.prescription_date or self.created_at.date()
            
        for med in self.medicines.all():
            if med.duration_days:
                end_date = p_date + timedelta(days=med.duration_days)
                if end_date >= timezone.now().date():
                    has_active_meds = True
                    break
            else:
                has_active_meds = True # Ongoing without specific duration
        
        if not has_active_meds and self.medicines.exists():
            self.status = 'expired'
            self.save()
        elif has_active_meds and self.status != 'active':
            self.status = 'active'
            self.save()

    def __str__(self):
        return f"Prescription {self.id} for {self.patient.username}"


class PrescribedMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, null=True, blank=True)
    frequency = models.CharField(max_length=100, null=True, blank=True)
    duration_days = models.IntegerField(null=True, blank=True)
    instructions = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.dosage}"
