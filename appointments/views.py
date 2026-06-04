from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer, PatientAppointmentSerializer
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth


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

            # Preserve authenticated patient identity when available.
            payload = request.data.copy()
            if request.user and request.user.is_authenticated:
                if not payload.get('user'):
                    payload['user'] = request.user.id
                if not payload.get('patient_email') and getattr(request.user, 'email', None):
                    payload['patient_email'] = request.user.email

                patient_name = payload.get('patient_name')
                if not patient_name or patient_name.strip() in ['', 'Demo Patient', 'User', 'Patient']:
                    first_name = getattr(request.user, 'first_name', '') or ''
                    last_name = getattr(request.user, 'last_name', '') or ''
                    full_name = f"{first_name} {last_name}".strip()
                    if not full_name:
                        full_name = getattr(request.user, 'full_name', None) or getattr(request.user, 'username', None) or payload.get('patient_email')
                    payload['patient_name'] = full_name or payload.get('patient_name')

            serializer = AppointmentSerializer(data=payload)
            
            if serializer.is_valid():
                appt = serializer.save(
                    doctor=slot.doctor,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    slot=slot
                )

                # Do not reserve the slot until the doctor accepts the request.
                # This keeps Addslot unchanged until confirmation.
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

    queryset = Appointment.objects.all().select_related('doctor', 'slot')

    if doctor_id:
        queryset = queryset.filter(doctor_id=doctor_id)

    if date:
        queryset = queryset.filter(start_time__date=date)

    if status_filter:
        queryset = queryset.filter(status=status_filter.lower())

    serializer = AppointmentSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pending_appointments(request):
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return Response({"error": "doctor_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    appointments = Appointment.objects.filter(doctor_id=doctor_id, status='pending').select_related('doctor', 'slot').order_by('-created_at')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recent_patients(request):
    """
    Get patients who have already visited/completed consultation.
    Filter by status='outpatient'.
    """
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return Response({"error": "doctor_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Recently visited means status is 'outpatient'
    appointments = Appointment.objects.filter(
        doctor_id=doctor_id, 
        status='outpatient'
    ).select_related('doctor', 'slot').order_by('-start_time')
    
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_history(request):
    """
    Get all previous appointments for a specific patient identified by email or phone.
    """
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    
    if not email and not phone:
        return Response({"error": "email or phone is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    query = Q()
    if email:
        query |= Q(patient_email=email)
    if phone:
        query |= Q(patient_phone=phone)
        
    appointments = Appointment.objects.filter(query).select_related('doctor', 'slot').order_by('-start_time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


from django.conf import settings
from django.core.mail import send_mail
from Notifications.models import Notification
from AdminLogin.models import User

def notify_appointment_change(appt, title, message):
    user_obj = None
    
    # 1. Try to find user by linked ID
    if appt.user:
        try:
            user_obj = User.objects.get(id=appt.user)
        except User.DoesNotExist:
            pass
            
    # 2. If not found, try to find user by email
    if not user_obj and appt.patient_email:
        try:
            user_obj = User.objects.get(email=appt.patient_email)
        except User.DoesNotExist:
            pass

    # 3. Create App Notification if user exists
    if user_obj:
        Notification.objects.create(user=user_obj, title=title, message=message)

    # 4. Send Email
    recipient = appt.patient_email or (user_obj.email if user_obj else None)
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

    # Prevent accepting if the requested slot has already been booked by another confirmation.
    if appt.slot and appt.slot.is_booked:
        return Response({"error": "Requested slot has already been booked"}, status=status.HTTP_400_BAD_REQUEST)

    # Update clinical details if provided during acceptance
    location = request.data.get("location")
    appt_type = request.data.get("appointment_type")
    
    if location: appt.location = location
    if appt_type: appt.appointment_type = appt_type

    appt.status = "confirmed"
    appt.save()

    if appt.slot:
        appt.slot.is_booked = True
        appt.slot.save()

    # Send Notification
    notify_appointment_change(
        appt, 
        "Appointment Confirmed", 
        f"Appointment booked with Dr. {appt.doctor.first_name} {appt.doctor.last_name}"
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
        "Appointment Rejection", 
        f"Your appointment with Dr. {appt.doctor.first_name} {appt.doctor.last_name} has been rejected. Reason: {reason}"
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


# 👤 PATIENT VIEW - Get patient's appointments
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_appointments(request):
    """
    Get all appointments for the authenticated patient/user.
    
    Query Parameters:
    - status: Filter by appointment status (pending, confirmed, booked, cancelled, rejected, outpatient)
    - date_from: Filter appointments from this date (YYYY-MM-DD format)
    - date_to: Filter appointments until this date (YYYY-MM-DD format)
    
    Returns:
    - List of appointments with doctor details, sorted by appointment date
    """
    from django.utils import timezone
    from datetime import datetime
    
    user = request.user
    
    # Filter appointments for the current user/patient
    # Match by user ID or email
    queryset = Appointment.objects.filter(
        Q(user=user.id) | Q(patient_email=user.email)
    ).select_related('doctor', 'slot').order_by('-start_time')
    
    # Apply optional filters
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter.lower())
    
    date_from = request.GET.get('date_from')
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            queryset = queryset.filter(start_time__date__gte=date_from_obj)
        except ValueError:
            return Response(
                {"error": "Invalid date format for date_from. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    date_to = request.GET.get('date_to')
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            queryset = queryset.filter(start_time__date__lte=date_to_obj)
        except ValueError:
            return Response(
                {"error": "Invalid date format for date_to. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if not queryset.exists():
        return Response({
            "message": "No appointments found",
            "appointments": []
        })
    
    serializer = PatientAppointmentSerializer(queryset, many=True)
    return Response({
        "message": "Appointments retrieved successfully",
        "count": queryset.count(),
        "appointments": serializer.data
    })


# 📋 Get single appointment details for patient
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_appointment_detail(request, id):
    """
    Get detailed information about a specific appointment for the patient.
    
    Returns:
    - Appointment details with full doctor information and slot details
    """
    user = request.user
    
    try:
        appt = Appointment.objects.get(
            (Q(user=user.id) | Q(patient_email=user.email)) & Q(id=id)
        )
    except Appointment.DoesNotExist:
        return Response(
            {"error": "Appointment not found or you don't have permission to view it"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PatientAppointmentSerializer(appt)
    return Response({
        "message": "Appointment details retrieved successfully",
        "appointment": serializer.data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_appointment(request, id):
    """
    Mark an appointment as completed (status = 'outpatient').
    """
    try:
        appointment = Appointment.objects.get(id=id)
        appointment.status = 'outpatient'
        appointment.save()
        
        return Response({
            "message": "Consultation completed successfully",
            "status": "outpatient"
        }, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_gender_stats(request):
    """
    Get patient analytics by gender for the admin dashboard.
    Returns counts of male and female patients per month for the current year.
    """
    from datetime import datetime
    current_year = datetime.now().year
    
    stats = Appointment.objects.filter(start_time__year=current_year).annotate(
        month_trunc=TruncMonth('start_time')
    ).values('month_trunc', 'patient_gender').annotate(
        count=Count('id')
    ).order_by('month_trunc')
    
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data_map = {i: {"male": 0, "female": 0} for i in range(1, 13)}
    
    for s in stats:
        if s['month_trunc']:
            m = s['month_trunc'].month
            gender = (s['patient_gender'] or "").lower()
            if "male" == gender:
                data_map[m]["male"] += s['count']
            elif "female" == gender:
                data_map[m]["female"] += s['count']
    
    result = []
    for i in range(1, 13):
        result.append({
            "month": month_names[i-1],
            "male": data_map[i]["male"],
            "female": data_map[i]["female"]
        })
        
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_analytics_summary(request):
    """
    Get summary percentages and weekly trends for gender distribution.
    """
    from django.utils import timezone
    from datetime import timedelta
    
    total = Appointment.objects.count()
    if total == 0:
        return Response({
            "male_pct": 0,
            "female_pct": 0,
            "weekly_male": [],
            "weekly_female": []
        })
    
    male_count = Appointment.objects.filter(patient_gender__iexact='male').count()
    female_count = Appointment.objects.filter(patient_gender__iexact='female').count()
    
    today = timezone.now().date()
    weekly_male = []
    weekly_female = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        m_count = Appointment.objects.filter(start_time__date=day, patient_gender__iexact='male').count()
        f_count = Appointment.objects.filter(start_time__date=day, patient_gender__iexact='female').count()
        weekly_male.append({"day": days[day.weekday()], "value": m_count})
        weekly_female.append({"day": days[day.weekday()], "value": f_count})
        
    return Response({
        "male_pct": round((male_count / total) * 100, 2),
        "female_pct": round((female_count / total) * 100, 2),
        "weekly_male": weekly_male,
        "weekly_female": weekly_female
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get monthly statistics for the doctor's activity chart.
    """
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return Response({"error": "doctor_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    from datetime import datetime
    current_year = datetime.now().year
    
    stats = Appointment.objects.filter(
        doctor_id=doctor_id,
        start_time__year=current_year
    ).annotate(
        month_trunc=TruncMonth('start_time')
    ).values('month_trunc').annotate(
        consultations=Count('id'),
        patients=Count('patient_email', distinct=True)
    ).order_by('month_trunc')
    
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    stats_dict = {s['month_trunc'].month: s for s in stats if s['month_trunc']}
    
    data = []
    for i in range(1, 13):
        m_stat = stats_dict.get(i, {'consultations': 0, 'patients': 0})
        data.append({
            "month": month_names[i-1],
            "Consultations": m_stat['consultations'],
            "Patients": m_stat['patients']
        })
        
    return Response(data)