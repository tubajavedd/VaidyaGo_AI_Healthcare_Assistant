from django.contrib import admin
from .models import Patient, DailySymptomVitals

admin.site.register(Patient)
admin.site.register(DailySymptomVitals)