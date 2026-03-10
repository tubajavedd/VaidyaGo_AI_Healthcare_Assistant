from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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
