from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer


# 🔹 CREATE

from django.db import transaction
from DoctorSlot.models import TimeSlot

@api_view(['POST'])
def create_appointment(request):
    slot_id = request.data.get("slot")

    if not slot_id:
        return Response({"error": "slot is required"}, status=400)

    try:
        with transaction.atomic():  # 🔒 START TRANSACTION

            # 🔒 LOCK THE SLOT
            slot = TimeSlot.objects.select_for_update().get(id=slot_id)

            # ❗ check if slot already booked
            if slot.is_booked:
                return Response({"error": "Slot already booked"}, status=400)

            serializer = AppointmentSerializer(data=request.data)

            if serializer.is_valid():
                appt = serializer.save(
                    doctor=slot.doctor,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    slot=slot
                )

                # ✅ mark slot booked
                slot.is_booked = True
                slot.save()

                return Response(serializer.data)

            return Response(serializer.errors)

    except TimeSlot.DoesNotExist:
        return Response({"error": "Invalid slot"}, status=404)


# 🔹 LIST
@api_view(['GET'])
def list_appointments(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')

    queryset = Appointment.objects.all()

    if doctor_id:
        queryset = queryset.filter(doctor_id=doctor_id)

    if date:
        queryset = queryset.filter(start_time__date=date)

    serializer = AppointmentSerializer(queryset, many=True)
    return Response(serializer.data)


# 🔹 CANCEL
@api_view(['PATCH'])
def cancel_appointment(request, id):
    try:
        appt = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if appt.status == "cancelled":
        return Response({"error": "Already cancelled"}, status=400)

    appt.status = "cancelled"
    appt.save()

    return Response({"message": "Appointment cancelled"})

#reschedule the appointments

@api_view(['PATCH'])
def reschedule_appointment(request, id):
    try:
        appt = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    # get new times
    new_start = request.data.get("start_time")
    new_end = request.data.get("end_time")

    if not new_start or not new_end:
        return Response(
            {"error": "start_time and end_time required"},
            status=400
        )

    # convert to datetime
    from datetime import datetime
    try:
        new_start = datetime.fromisoformat(new_start)
        new_end = datetime.fromisoformat(new_end)
    except:
        return Response({"error": "Invalid datetime format"}, status=400)

    # ❗ conflict check (exclude current appointment)
    conflict = Appointment.objects.filter(
        doctor=appt.doctor,
        start_time__lt=new_end,
        end_time__gt=new_start,
        status='booked'
    ).exclude(id=appt.id).exists()

    if conflict:
        return Response(
            {"error": "New slot already booked"},
            status=400
        )

    # update
    appt.start_time = new_start
    appt.end_time = new_end
    appt.save()

    return Response({"message": "Appointment rescheduled"})