from django.contrib import admin
from .models import Medication, Pharmacy, PrescriptionRequest

admin.site.register(Medication)
admin.site.register(Pharmacy)
admin.site.register(PrescriptionRequest)
