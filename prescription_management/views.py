import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Prescription, PrescribedMedicine
from .serializers import PrescriptionSerializer, PrescriptionUploadSerializer
from .ocr_service import OCRService
from django.utils import timezone
from datetime import datetime, date, timedelta

from TodaySchedule_medication.models import Schedule
from reminder.models import Reminder
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class PrescriptionUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def is_covid_document(self, extracted_data, file_name=None):
        if not extracted_data:
            return False

        lower = lambda value: (value or '').__str__().lower()
        check_values = [
            lower(extracted_data.get('document_type')),
            lower(extracted_data.get('document_name')),
            lower(extracted_data.get('summary')),
            lower(extracted_data.get('doctor_name')),
            lower(extracted_data.get('hospital_name')),
            lower(file_name),
        ]

        findings = extracted_data.get('findings')
        if isinstance(findings, list):
            check_values.append(' '.join(str(x).lower() for x in findings))
        else:
            check_values.append(lower(findings))

        test_results = extracted_data.get('test_results')
        if isinstance(test_results, list):
            check_values.append(' '.join(str(x).lower() for x in test_results))
        else:
            check_values.append(lower(test_results))

        combined = ' '.join(value for value in check_values if value)
        return 'covid' in combined

    def post(self, request):
        images = request.FILES.getlist('image')
        files = request.FILES.getlist('file')
        documents = []
        
        for img in images:
            documents.append(('image', img))
        for f in files:
            documents.append(('file', f))
            
        if not documents:
            # Fallback to single file from data if getlist is empty
            serializer = PrescriptionUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data.get('image'):
                documents.append(('image', serializer.validated_data['image']))
            elif serializer.validated_data.get('file'):
                documents.append(('file', serializer.validated_data['file']))
                
        if not documents:
             return Response({"error": "No image or file provided."}, status=status.HTTP_400_BAD_REQUEST)

        restrict_to = request.data.get('restrict_to')
        processed_prescriptions = []
        extraction_summaries = []

        for doc_type, doc in documents:
            # 1. Create Prescription record
            prescription = Prescription(patient=request.user, status='active')
            if doc_type == 'image':
                prescription.image = doc
            else:
                prescription.file = doc
            prescription.save()
            
            # 2. Extract Text via OCR
            file_path = prescription.image.path if prescription.image else prescription.file.path
            extracted_data = OCRService.extract_prescription_details(file_path)
            
            # Ensure extracted_data is never None
            if extracted_data is None:
                extracted_data = OCRService.normalize_extracted_data(None)
                
            print("EXTRACTED DATA IN VIEW:")
            print(extracted_data)
            print("-" * 50)

            if restrict_to == 'covid' and not self.is_covid_document(extracted_data, doc.name):
                prescription.delete()
                return Response({"error": "Please upload COVID-19 reports here only."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Prepare extraction summary for response
            extraction_summary = {
                "document_type": extracted_data.get("document_type"),
                "doctor_name": extracted_data.get("doctor_name"),
                "hospital_name": extracted_data.get("hospital_name"),
                "report_date": extracted_data.get("report_date") or extracted_data.get("prescription_date"),
                "patient_name": extracted_data.get("patient_name"),

                "summary": extracted_data.get("summary"),

                "findings": extracted_data.get("findings", []),

                "medicines_count": len(extracted_data.get("medicines", [])),
                "medicines": extracted_data.get("medicines", []),

                "test_results": extracted_data.get("test_results", []),

                "recommendations": extracted_data.get("recommendations", []),

                "special_instructions": extracted_data.get("special_instructions")
            }
            
            if extracted_data:
                # 3. Update Prescription details
                prescription.doctor_name = extracted_data.get('doctor_name', '')
                prescription.hospital_name = extracted_data.get('hospital_name', '')
                
                p_date = extracted_data.get('prescription_date')
                if p_date:
                    try:
                        prescription.prescription_date = datetime.strptime(p_date, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                        
                prescription.extracted_patient_name = extracted_data.get('patient_name', '')
                prescription.document_type = extracted_data.get('document_type', 'Medical Document')
                prescription.document_name = extracted_data.get('document_name') or extracted_data.get('document_type', 'Medical Document')
                prescription.special_instructions = extracted_data.get('special_instructions', '')
                prescription.save()
                
                # Update extraction summary
                extraction_summary = {
                    "document_type": extracted_data.get("document_type"),

                    "doctor_name": extracted_data.get("doctor_name"),
                    "hospital_name": extracted_data.get("hospital_name"),

                    "report_date": extracted_data.get("report_date"),
                    "prescription_date": extracted_data.get("prescription_date"),

                    "patient_name": extracted_data.get("patient_name"),

                    "summary": extracted_data.get("summary"),

                    "findings": extracted_data.get("findings", []),

                    "medicines_count": len(extracted_data.get("medicines", [])),
                    "medicines": extracted_data.get("medicines", []),

                    "test_results": extracted_data.get("test_results", []),

                    "recommendations": extracted_data.get("recommendations", []),

                    "special_instructions": extracted_data.get("special_instructions")
                }
                
                # 4. Create Medicines and Schedules
                medicines_data = extracted_data.get('medicines') or []
                for med in medicines_data:
                    pm = PrescribedMedicine.objects.create(
                        prescription=prescription,
                        name=med.get('name') or 'Unknown Medicines',
                        dosage=med.get('dosage')or'',
                        frequency=med.get('frequency')or'',
                        duration_days=med.get('duration_days'),
                        instructions=med.get('instructions')or ''
                    )
                    
                    # 5. Generate Medicine Schedule
                    self.generate_schedule(request.user, pm)
                    self.create_medication_reminder(request.user, pm)

                prescription.update_status()
            
            extraction_summaries.append(extraction_summary)
            processed_prescriptions.append(prescription)

        if len(processed_prescriptions) == 1:
            return Response(
                {
                    "message": "Prescription uploaded and processed successfully",
                    "extraction_details": extraction_summaries[0]
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "message": f"{len(processed_prescriptions)} Prescriptions uploaded and processed successfully",
                    "extraction_details": extraction_summaries
                },
                status=status.HTTP_201_CREATED
            )

    def generate_schedule(self, user, medicine):
        # Basic scheduling logic based on frequency
        freq = medicine.frequency.lower() if medicine.frequency else ''
        times = []
        if 'once' in freq or '1-0-0' in freq or '0-0-1' in freq:
            times = ['08:00:00'] if '1-0-0' in freq else ['20:00:00']
        elif 'twice' in freq or '1-0-1' in freq:
            times = ['08:00:00', '20:00:00']
        elif 'thrice' in freq or '1-1-1' in freq:
            times = ['08:00:00', '14:00:00', '20:00:00']
        else:
            times = ['09:00:00'] # Default fallback
            
        freq_choice = 'Once Daily'
        if len(times) == 2: freq_choice = 'Twice Daily'
        elif len(times) == 3: freq_choice = 'Thrice Daily'
            
        for t in times:
            Schedule.objects.create(
                patient=user,
                medication_name=medicine.name,
                dosage=medicine.dosage or '',
                frequency=freq_choice,
                time=t,
                routine_type='Routine'
            )



    def create_medication_reminder(self, user, pm):
        """
        Automatically creates a Reminder object based on the prescribed medicine's frequency.
        """
        from reminder.views import TIME_MAP
        from datetime import date
        
        freq = pm.frequency.lower() if pm.frequency else ''
        reminder_times = []
        
        if 'once' in freq or '1-0-0' in freq:
            reminder_times = ['morning']
        elif '0-0-1' in freq:
            reminder_times = ['night']
        elif 'twice' in freq or '1-0-1' in freq:
            reminder_times = ['morning', 'night']
        elif 'thrice' in freq or '1-1-1' in freq:
            reminder_times = ['morning', 'afternoon', 'night']
        elif 'evening' in freq:
            reminder_times = ['evening']
        else:
            reminder_times = ['morning']
            
        start_date = date.today()
        duration = pm.duration_days or 7
        end_date = start_date + timedelta(days=duration)
        
        first_time_str = TIME_MAP.get(reminder_times[0], "08:00")
        try:
            trigger_time = datetime.strptime(first_time_str, "%H:%M").time()
            next_trigger = datetime.combine(start_date, trigger_time)
        except Exception:
            next_trigger = timezone.now()
            
        Reminder.objects.create(
            user=user,
            medicine_name=pm.name,
            dosage=pm.dosage or '',
            frequency=pm.frequency or 'Daily',
            duration_days=duration,
            times=reminder_times,
            start_date=start_date,
            end_date=end_date,
            next_trigger=next_trigger
        )
class PrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Update statuses before returning
        qs = Prescription.objects.filter(patient=self.request.user).order_by('-created_at')
        for p in qs:
            p.update_status()
        return qs


class ActivePrescriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        active_prescriptions = Prescription.objects.filter(patient=request.user, status='active').order_by('-created_at')
        for p in active_prescriptions:
            p.update_status()
            
        # Re-fetch after update
        active_prescription = Prescription.objects.filter(patient=request.user, status='active').order_by('-created_at').first()
        
        if active_prescription:
            serializer = PrescriptionSerializer(active_prescription)
            return Response(serializer.data)
        return Response({"message": "No active prescription found"}, status=status.HTTP_404_NOT_FOUND)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. Active Prescription
        active_p = Prescription.objects.filter(patient=user, status='active').order_by('-created_at').first()
        active_p_data = PrescriptionSerializer(active_p).data if active_p else None
        
        # 2. Today's Medicines
        today = timezone.now().date()
        schedules = Schedule.objects.filter(patient=user, date=today).order_by('time')
        
        today_meds = []
        next_med = None
        now_time = timezone.now().time()
        
        for sch in schedules:
            med_data = {
                "id": sch.id,
                "name": sch.medication_name,
                "time": sch.time.strftime('%H:%M'),
                "is_taken": sch.is_taken
            }
            today_meds.append(med_data)
            
            if not sch.is_taken and not next_med and sch.time > now_time:
                next_med = med_data
                
        # 3. Prescription History Summary
        total = Prescription.objects.filter(patient=user).count()
        completed = Prescription.objects.filter(patient=user, status='completed').count()
        
        return Response({
            "active_prescription": active_p_data,
            "today_medicines": today_meds,
            "next_medicine": next_med,
            "history_summary": {
                "total": total,
                "completed": completed
            }
        })
class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific prescription.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        return Prescription.objects.filter(patient=self.request.user)
