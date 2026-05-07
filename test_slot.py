import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from DoctorSlot.models import TimeSlot
from Dr_personalInfo.models import DoctorPersonalInfo
from django.utils import timezone
from datetime import timedelta

def test_add_slot():
    try:
        doctor = DoctorPersonalInfo.objects.first()
        if not doctor:
            print("No doctor found in Dr_personalInfo_doctorpersonalinfo")
            return
            
        print(f"Adding slot for doctor: {doctor} (ID: {doctor.id})")
        
        slot = TimeSlot.objects.create(
            doctor=doctor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            is_booked=False
        )
        print(f"Successfully created slot: {slot}")
    except Exception as e:
        print(f"Error creating slot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_add_slot()
