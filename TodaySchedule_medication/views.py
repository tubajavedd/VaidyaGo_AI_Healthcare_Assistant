from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Schedule, User
from rest_framework import status
from .serializers import ScheduleSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class AddScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(
                {
                    "message": "Schedule added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#todays's schedule(only pending)
class TodayScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        schedules = Schedule.objects.filter(
            patient=request.user,
            date=today,
            is_taken=False
        )

        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
#mark as taken
class MarkTakenView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request, pk):
        try:
            schedule = Schedule.objects.get(id=pk, patient=request.user)
        except Schedule.DoesNotExist:
            return Response({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        
        schedule.is_taken = True
        schedule.save()
        return Response({"message": "Medication marked as taken"}, status=status.HTTP_200_OK)