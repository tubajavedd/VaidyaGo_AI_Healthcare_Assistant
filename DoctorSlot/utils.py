from datetime import datetime, timedelta, time
from django.utils import timezone

from Dr_personalInfo.models import DoctorPersonalInfo
from DoctorSlot.models import TimeSlot

def generate_slots_for_week():
    doctors = DoctorPersonalInfo.objects.all()
    today = timezone.now().date()
    start_of_week = today + timedelta(days=(7 - today.weekday()))

    for doctor in doctors:
        for day in range(6):  # Monday–Saturday
            current_date = start_of_week + timedelta(days=day)
            generate_time_slots(doctor, current_date, time(10, 0), time(13, 0))  # Morning
            generate_time_slots(doctor, current_date, time(16, 0), time(19, 0))  # Evening

def generate_time_slots(doctor, date, start, end):
    current = timezone.make_aware(datetime.combine(date, start))
    end_time = timezone.make_aware(datetime.combine(date, end))

    while current < end_time:
        slot_end = current + timedelta(minutes=30)
        exists = TimeSlot.objects.filter(doctor=doctor, start_time=current).exists()
        if not exists:
            TimeSlot.objects.create(doctor=doctor, start_time=current, end_time=slot_end)
        current = slot_end

def print_all_slots():
    """
    Prints all slots, grouped by doctor, and shows booked/available.
    """
    doctors = DoctorPersonalInfo.objects.all()
    for doctor in doctors:
        print(f"\n=== Doctor: {doctor.first_name} ===")
        slots = TimeSlot.objects.filter(doctor=doctor).order_by('start_time')
        for slot in slots:
            status = "Booked" if slot.is_booked else "Available"
            print(f"ID: {slot.id} | {slot.start_time} - {slot.end_time} | {status}")