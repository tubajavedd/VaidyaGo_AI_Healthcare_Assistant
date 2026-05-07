from django.contrib import admin
from .models import PrescribedMedicine, Prescription

admin.site.register(PrescribedMedicine)
admin.site.register(Prescription)
