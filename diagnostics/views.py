from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Diagnostic
from .serializers import DiagnosticSerializer, DiagnosticRequestSerializer
from .services.diagnostic_service import DiagnosticService
from .utils.response import success_response, error_response

class DiagnosticAnalyzeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DiagnosticRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            service = DiagnosticService()
            diagnosis, was_cached = service.get_or_create_diagnosis(
                request.user,
                **serializer.validated_data
            )
            
            response_data = DiagnosticSerializer(diagnosis).data
            response_data['cached'] = was_cached
            
            return success_response(response_data, "Diagnostic analysis completed")
        except Exception as e:
            return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiagnosticHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        history = Diagnostic.objects.filter(user=request.user)
        serializer = DiagnosticSerializer(history, many=True)
        return success_response(serializer.data, "History retrieved successfully")

class DiagnosticDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            diagnosis = Diagnostic.objects.get(pk=pk, user=request.user)
            serializer = DiagnosticSerializer(diagnosis)
            return success_response(serializer.data, "Detail retrieved successfully")
        except Diagnostic.DoesNotExist:
            return error_response("Diagnostic not found", status.HTTP_404_NOT_FOUND)

class DiagnosticByBodyPartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, body_part):
        diagnoses = Diagnostic.objects.filter(user=request.user, body_part__iexact=body_part)
        serializer = DiagnosticSerializer(diagnoses, many=True)
        return success_response(serializer.data, f"Diagnoses for {body_part} retrieved")
