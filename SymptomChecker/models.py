from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=20, unique=True)  # e.g., PX-8829
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.patient_id})"

class DailySymptomVitals(models.Model):
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='symptom_entries')
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Primary complaints (matching the edit form)
    headache_duration = models.CharField(max_length=50)
    headache_severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    fatigue_duration = models.CharField(max_length=50)
    fatigue_severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    eye_strain_duration = models.CharField(max_length=50)
    eye_strain_severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)

    # Vitals
    temperature_f = models.DecimalField(max_digits=5, decimal_places=1)
    heart_rate_bpm = models.PositiveSmallIntegerField()

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return f"{self.patient.patient_id} – {self.date}"

class SavedReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='saved_reports')
    condition_name = models.CharField(max_length=200)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=1)  # e.g., 94.2
    report_snapshot = models.JSONField()  # store the entire report details (description, explanation, etc.)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} – {self.condition_name} ({self.saved_at.date()})"

class SymptomAuditLog(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='audit_logs')
    active_symptoms = models.JSONField(default=list)   # e.g., ["Sneezing", "Nasal Congestion"]
    severity = models.PositiveSmallIntegerField()      # 0-10
    environmental_triggers = models.JSONField(default=list)  # e.g., ["Dust", "Pollen"]
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} – Log {self.created_at.date()}"

class MedicationDose(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_doses')
    medication_name = models.CharField(max_length=200)  # e.g., "Fluticasone Propionate (Nasal Spray)"
    instructions = models.TextField(blank=True)         # e.g., "2 Sprays in each nostril"
    time_taken = models.TimeField()
    date_taken = models.DateField()
    observation_notes = models.TextField(blank=True)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} – {self.medication_name} on {self.date_taken} at {self.time_taken}"

















# from django.db import models
# from django.conf import settings

# class SymptomLog(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     symptoms = models.TextField(help_text="Comma-separated symptoms or description")
#     diagnosis = models.TextField(blank=True, null=True)
#     recommended_action = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Log {self.id} - {self.user}"
