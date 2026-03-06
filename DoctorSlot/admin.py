from django.apps import AppConfig

class DoctorSlotConfig(AppConfig):   # ✅ EXACT NAME
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DoctorSlot'
