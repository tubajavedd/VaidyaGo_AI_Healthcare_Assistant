from django.contrib import admin
from .models import Doctor, PastMedication

admin.site.register(Doctor)
admin.site.register(PastMedication)
