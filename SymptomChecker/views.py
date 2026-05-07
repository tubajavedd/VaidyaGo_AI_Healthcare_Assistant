from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .serializers import SymptomVitalsSerializer, PatientSummarySerializer, SavedReportSerializer, SymptomAuditLogSerializer, MedicationDoseSerializer
from .models import Patient, DailySymptomVitals, SavedReport, SymptomAuditLog, MedicationDose
from .diagnostic_engine import run_diagnostic_engine, get_condition_details

class PatientSummaryView(APIView):
    permission_classes = [AllowAny]  # override default IsAuthenticated for now

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        serializer = PatientSummarySerializer(patient)
        return Response(serializer.data)

class UpdateInputSummaryView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        serializer = SymptomVitalsSerializer(data=request.data)
        if serializer.is_valid():
            new_entry = DailySymptomVitals.objects.create(
                patient=patient,
                **serializer.validated_data
            )
            diagnostic_results = run_diagnostic_engine(new_entry)
            return Response({
                "message": "Symptoms and vitals saved successfully",
                "updated_summary": serializer.data,
                "diagnostic_results": diagnostic_results
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConditionDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patient_id, condition_name):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        details = get_condition_details(patient, condition_name)
        if not details:
            return Response({"error": "Condition not found or no symptom data available"}, status=404)
        return Response(details)

class SaveReportView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        condition_name = request.data.get('condition_name')
        confidence_score = request.data.get('confidence_score')
        report_snapshot = request.data.get('report_snapshot')  # the entire report details

        if not condition_name or not report_snapshot:
            return Response({"error": "condition_name and report_snapshot are required"}, status=400)

        saved = SavedReport.objects.create(
            patient=patient,
            condition_name=condition_name,
            confidence_score=confidence_score,
            report_snapshot=report_snapshot
        )
        serializer = SavedReportSerializer(saved)
        return Response({"message": "Result Saved to Record", "saved_report": serializer.data}, status=201)

class SymptomAuditLogView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        serializer = SymptomAuditLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response({
                "message": "Symptom Log Saved",
                "log_entry": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Optional: GET to retrieve all logs for this patient
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        logs = patient.audit_logs.all().order_by('-created_at')
        serializer = SymptomAuditLogSerializer(logs, many=True)
        return Response(serializer.data)

class ConfirmMedicationDoseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        serializer = MedicationDoseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response({
                "message": "Medication dose confirmed successfully",
                "dose": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Optional: get all confirmed doses for a patient
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        doses = patient.medication_doses.all().order_by('-date_taken', '-time_taken')
        serializer = MedicationDoseSerializer(doses, many=True)
        return Response(serializer.data)























# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import SymptomLog
# from .serializers import SymptomLogSerializer
# from .diagnostic_engine import analyze_symptoms

# class SymptomLogViewSet(viewsets.ModelViewSet):
#     queryset = SymptomLog.objects.all().order_by('-created_at')
#     serializer_class = SymptomLogSerializer

#     def perform_create(self, serializer):
#         user = self.request.user if self.request.user.is_authenticated else None
#         serializer.save(user=user)

#     @action(detail=False, methods=['post'])
#     def analyze(self, request):
#         symptoms = request.data.get('symptoms')
#         if not symptoms:
#             return Response({"error": "Symptoms are required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Analyze symptoms using the diagnostic engine
#         result = analyze_symptoms(symptoms)
        
#         # Save to database
#         user = request.user if request.user.is_authenticated else None
#         log = SymptomLog.objects.create(
#             user=user,
#             symptoms=symptoms,
#             diagnosis=result.get("diagnosis", ""),
#             recommended_action=result.get("recommended_action", "")
#         )
        
#         serializer = self.get_serializer(log)
#         return Response(serializer.data, status=status.HTTP_200_OK)
