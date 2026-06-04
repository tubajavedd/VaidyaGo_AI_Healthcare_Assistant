from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# DoctorSlot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
from DoctorSlot.utils import generate_slots_for_week
from .models import TimeSlot, DoctorSlot


@csrf_exempt
def generate_slots_api(request):
    if request.method == "POST":
        generate_slots_for_week()
        return JsonResponse({"message": "Slots generated successfully"})
    return JsonResponse({"error": "Invalid method"}, status=400)



class GenerateSlotsAPI(APIView):
    def post(self, request):
        try:
            generate_slots_for_week()
            return Response({
                "message": "Slots generated successfully"
            })
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)



from .models import DoctorSlot
from .serializers import DoctorSlotSerializer


class DoctorSlotListCreateAPI(APIView):

    def get(self, request):
        slots = DoctorSlot.objects.filter(is_active=True)
        doctor_id = request.query_params.get('doctor')
        if doctor_id:
            slots = slots.filter(doctor_id=doctor_id)
        serializer = DoctorSlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSlotSerializer(data=request.data)
        if serializer.is_valid():
            doctor_slot = serializer.save()
            from .utils import generate_timeslots_from_template
            generate_timeslots_from_template(doctor_slot)
            return Response(
                {"message": "Doctor slot created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorSlotDetailAPI(APIView):

    def get(self, request, pk):
        slot = get_object_or_404(DoctorSlot, pk=pk)
        serializer = DoctorSlotSerializer(slot)
        return Response(serializer.data)

    def put(self, request, pk):
        slot = get_object_or_404(DoctorSlot, pk=pk)
        serializer = DoctorSlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor slot updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        slot = get_object_or_404(DoctorSlot, pk=pk)
        serializer = DoctorSlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor slot partially updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        slot = get_object_or_404(DoctorSlot, pk=pk)
        slot.delete()
        return Response(
            {"message": "Doctor slot deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

#see all slots

from DoctorSlot.models import TimeSlot
from Dr_personalInfo.models import DoctorPersonalInfo

def doctor_slots_api(request, doctor_id):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        doctor = DoctorPersonalInfo.objects.get(id=doctor_id)
    except DoctorPersonalInfo.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)

    # check if query param ?booked=true or false
    booked_param = request.GET.get("booked")
    if booked_param == "true":
        slots = TimeSlot.objects.filter(doctor=doctor, is_booked=True)
    elif booked_param == "false":
        slots = TimeSlot.objects.filter(doctor=doctor, is_booked=False)
    else:
        slots = TimeSlot.objects.filter(doctor=doctor)

    data = [
        {
            "id": slot.id,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "is_booked": slot.is_booked
        }
        for slot in slots
    ]
    return JsonResponse({"doctor_id": doctor_id, "slots": data})




from .serializers import TimeSlotSerializer

class DoctorBookedSlotsAPI(APIView):
    """
    Return only booked slots for a specific doctor
    """
    def get(self, request, doctor_id):
        try:
            doctor = DoctorPersonalInfo.objects.get(id=doctor_id)
        except DoctorPersonalInfo.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        date_param = request.query_params.get('date')
        queryset = TimeSlot.objects.filter(doctor=doctor, is_booked=True)

        if date_param:
            queryset = queryset.filter(start_time__date=date_param)

        serializer = TimeSlotSerializer(queryset, many=True)
        return Response({
            "doctor_id": doctor_id,
            "date": date_param,
            "booked_slots": serializer.data
        })


class DoctorAllSlotsAPI(APIView):
    def get(self, request, doctor_id):
        date_param = request.query_params.get('date')
        booked_param = request.query_params.get('booked')

        queryset = TimeSlot.objects.filter(doctor_id=doctor_id)

        if booked_param == 'true':
            queryset = queryset.filter(is_booked=True)
        elif booked_param == 'false':
            queryset = queryset.filter(is_booked=False)

        if date_param:
            queryset = queryset.filter(start_time__date=date_param)

        serializer = TimeSlotSerializer(queryset, many=True)
        return Response({
            "doctor_id": doctor_id,
            "date": date_param,
            "slots": serializer.data
        })


class TimeSlotCreateAPI(APIView):
    """
    Allow doctor to manually add a single available time slot
    """
    def post(self, request):
        serializer = TimeSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Time slot created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
