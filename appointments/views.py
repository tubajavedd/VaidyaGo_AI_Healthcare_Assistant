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
        return Response({"error": "slot is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Lock the slot for update to prevent concurrent bookings
            slot = TimeSlot.objects.select_for_update().get(id=slot_id)

            if slot.is_booked:
                return Response({"error": "Slot already booked"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = AppointmentSerializer(data=request.data)
            
            if serializer.is_valid():
                appt = serializer.save(
                    doctor=slot.doctor,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    slot=slot
                )

                slot.is_booked = True
                slot.save()

                return Response(AppointmentSerializer(appt).data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except TimeSlot.DoesNotExist:
        return Response({"error": "Invalid slot"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_appointments(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    status_filter = request.GET.get('status')

    queryset = Appointment.objects.all()

    if doctor_id:
        queryset = queryset.filter(doctor_id=doctor_id)

    if date:
        queryset = queryset.filter(start_time__date=date)

    if status_filter:
        queryset = queryset.filter(status=status_filter.lower())

    serializer = AppointmentSerializer(queryset, many=True)
    return Response(serializer.data)


from django.conf import settings
from django.core.mail import send_mail
from Notifications.models import Notification
from AdminLogin.models import User

def notify_appointment_change(appt, title, message):
    # 1. Send App Notification (if user is linked)
    if appt.user:
        try:
            user_obj = User.objects.get(id=appt.user)
            Notification.objects.create(user=user_obj, title=title, message=message)
        except:
            pass

    # 2. Send Email
    recipient = appt.patient_email
    if not recipient and appt.user:
        try:
            user_obj = User.objects.get(id=appt.user)
            recipient = user_obj.email
        except:
            pass
            
    if recipient:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=True
        )


# 🔹 CANCEL
@api_view(['PATCH'])
def cancel_appointment(request, id):
    try:
        appt = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if appt.status == "cancelled":
        return Response({"error": "Already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

    reason = request.data.get("reason")
    appt.status = "cancelled"
    
    if reason:
        appt.rejection_reason = reason

    if appt.slot:
        appt.slot.is_booked = False
        appt.slot.save()
        
    appt.save()

    # Send Notification
    notify_appointment_change(
        appt, 
        "Appointment Cancelled", 
        f"Your appointment with Dr. {appt.doctor} has been cancelled. Reason: {reason or 'Not specified'}"
    )

    return Response({"message": "Appointment cancelled successfully"})


# 🔹 ACCEPT
@api_view(['PATCH'])
def accept_appointment(request, id):
    try:
        appt = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if appt.status == "confirmed":
        return Response({"error": "Already confirmed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update clinical details if provided during acceptance
    location = request.data.get("location")
    appt_type = request.data.get("appointment_type")
    
    if location: appt.location = location
    if appt_type: appt.appointment_type = appt_type

    appt.status = "confirmed"
    appt.save()

    # Send Notification
    notify_appointment_change(
        appt, 
        "Appointment Confirmed", 
        f"Your appointment request for Dr. {appt.doctor} has been confirmed. Location: {appt.location or 'Main Clinic'}"
    )

    return Response({
        "message": "Appointment confirmed successfully",
        "data": AppointmentSerializer(appt).data
    })


# 🔹 REJECT
@api_view(['PATCH'])
def reject_appointment(request, id):
    try:
        appt = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if appt.status == "rejected":
        return Response({"error": "Already rejected"}, status=status.HTTP_400_BAD_REQUEST)

    reason = request.data.get("reason")
    if not reason:
        return Response({"error": "Rejection reason is required"}, status=status.HTTP_400_BAD_REQUEST)

    appt.status = "rejected"
    appt.rejection_reason = reason
    
    if appt.slot:
        appt.slot.is_booked = False
        appt.slot.save()
        
    appt.save()

    # Send Notification
    notify_appointment_change(
        appt, 
        "Appointment Rejected", 
        f"Your appointment request with Dr. {appt.doctor} was declined. Clinical Note: {reason}"
    )

    return Response({"message": "Appointment rejected successfully"})


@api_view(['PATCH'])
def reschedule_appointment(request, id):
    try:
        appt = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    slot_id = request.data.get("slot")
    reason = request.data.get("reschedule_reason")

    if not slot_id:
        return Response({"error": "slot is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            old_slot = appt.slot
            
            try:
                new_slot = TimeSlot.objects.select_for_update().get(id=slot_id)
            except TimeSlot.DoesNotExist:
                return Response({"error": "Invalid slot ID"}, status=status.HTTP_404_NOT_FOUND)

            if new_slot.is_booked and new_slot != old_slot:
                return Response({"error": "New slot already booked"}, status=status.HTTP_400_BAD_REQUEST)

            appt.slot = new_slot
            appt.start_time = new_slot.start_time
            appt.end_time = new_slot.end_time
            appt.doctor = new_slot.doctor
            
            if reason:
                appt.reschedule_reason = reason

            appt.save()

            if old_slot and old_slot != new_slot:
                old_slot.is_booked = False
                old_slot.save()
            
            new_slot.is_booked = True
            new_slot.save()

            # Send Notification
            notify_appointment_change(
                appt, 
                "Appointment Rescheduled", 
                f"Your appointment with Dr. {appt.doctor} has been moved to {appt.start_time}. Reason: {reason or 'Not specified'}"
            )

            return Response({
                "message": "Appointment rescheduled successfully",
                "data": AppointmentSerializer(appt).data
            })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)