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

        # --- NEW: Auto-generate today's schedule from active prescription ---
        from prescription_management.models import Prescription
        active_p = Prescription.objects.filter(patient=request.user, status='active').order_by('-created_at').first()
        if active_p:
            active_p.update_status() # Ensure status is up-to-date
            if active_p.status == 'active':
                for med in active_p.medicines.all():
                    # Check if schedule for this med already exists today
                    if not Schedule.objects.filter(patient=request.user, medication_name=med.name, date=today).exists():
                        # Generate for today
                        freq = med.frequency.lower() if med.frequency else ''
                        times = []
                        if 'once' in freq or '1-0-0' in freq or '0-0-1' in freq:
                            times = ['08:00:00'] if '1-0-0' in freq else ['20:00:00']
                        elif 'twice' in freq or '1-0-1' in freq:
                            times = ['08:00:00', '20:00:00']
                        elif 'thrice' in freq or '1-1-1' in freq:
                            times = ['08:00:00', '14:00:00', '20:00:00']
                        else:
                            times = ['09:00:00']
                            
                        freq_choice = 'Once Daily'
                        if len(times) == 2: freq_choice = 'Twice Daily'
                        elif len(times) == 3: freq_choice = 'Thrice Daily'
                            
                        for t in times:
                            Schedule.objects.create(
                                patient=request.user,
                                medication_name=med.name,
                                dosage=med.dosage or '',
                                frequency=freq_choice,
                                time=t,
                                routine_type='Routine'
                            )
        # --------------------------------------------------------------------

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