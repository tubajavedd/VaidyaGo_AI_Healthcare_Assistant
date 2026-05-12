from django.db import models
from django.conf import settings

class Diagnostic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diagnostics')
    body_part = models.CharField(max_length=100)
    sub_region = models.CharField(max_length=100)
    symptoms = models.JSONField()
    duration = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    possible_diseases = models.JSONField()
    recommendations = models.JSONField()
    precautions = models.JSONField()
    consultation_advice = models.TextField()
    confidence_score = models.FloatField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.body_part} ({self.created_at})"
