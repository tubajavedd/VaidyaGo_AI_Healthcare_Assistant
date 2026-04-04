from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# DoctorSlot/views.py
from django.http import JsonResponse
from DoctorSlot.utils import generate_slots_for_week
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_slots_api(request):
    if request.method == "POST":
        generate_slots_for_week()
        return JsonResponse({"message": "Slots generated successfully"})
    return JsonResponse({"error": "Invalid method"}, status=400)

from .models import DoctorSlot
from .serializers import DoctorSlotSerializer


class DoctorSlotListCreateAPI(APIView):

    def get(self, request):
        slots = DoctorSlot.objects.filter(is_active=True)
        serializer = DoctorSlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
from django.http import JsonResponse
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


from DoctorSlot.models import TimeSlot
from Dr_personalInfo.models import DoctorPersonalInfo
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

        slots = TimeSlot.objects.filter(doctor=doctor, is_booked=True)
        serializer = TimeSlotSerializer(slots, many=True)
        return Response({
            "doctor_id": doctor_id,
            "booked_slots": serializer.data
        })


class DoctorAllSlotsAPI(APIView):
    def get(self, request, doctor_id):
        slots = TimeSlot.objects.filter(doctor_id=doctor_id)
        serializer = TimeSlotSerializer(slots, many=True)
        return Response({
            "doctor_id": doctor_id,
            "slots": serializer.data
        })
