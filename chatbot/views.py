import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.chatbot_engine import ChatbotEngine
from .services.tool_router import ToolRouter
from .services.tools_registry import ToolsRegistry
from .serializers import ChatRequestSerializer, ChatResponseSerializer

logger = logging.getLogger(__name__)


@api_view(["POST"])
def chat_view(request):
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": "Invalid request payload",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    message = serializer.validated_data.get("message", "").strip()
    session_id = serializer.validated_data.get("session_id")
    documents = request.FILES.getlist("documents") or request.FILES.getlist("document")
    user = request.user if request.user and request.user.is_authenticated else None

    # --- NEW: Handle Document/Prescription Upload via Chat ---
    if documents and user:
        from prescription_management.models import Prescription, PrescribedMedicine
        from prescription_management.ocr_service import OCRService
        from datetime import datetime
        from prescription_management.views import PrescriptionUploadView
        
        uploader_view = PrescriptionUploadView()
        success_count = 0
        
        for document in documents:
            prescription = Prescription.objects.create(
                patient=user,
                file=document,
                status='active'
            )
            
            extracted_data = OCRService.extract_prescription_details(prescription.file.path)
            if extracted_data:
                prescription.doctor_name = extracted_data.get('doctor_name', '')
                prescription.hospital_name = extracted_data.get('hospital_name', '')
                p_date = extracted_data.get('prescription_date')
                if p_date:
                    try:
                        prescription.prescription_date = datetime.strptime(p_date, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                prescription.extracted_patient_name = extracted_data.get('patient_name', '')
                prescription.special_instructions = extracted_data.get('special_instructions', '')
                prescription.save()
                
                medicines_data = extracted_data.get('medicines', [])
                for med in medicines_data:
                    pm = PrescribedMedicine.objects.create(
                        prescription=prescription,
                        name=med.get('name', 'Unknown'),
                        dosage=med.get('dosage', ''),
                        frequency=med.get('frequency', ''),
                        duration_days=med.get('duration_days'),
                        instructions=med.get('instructions', '')
                    )
                    uploader_view.generate_schedule(user, pm)
                
                prescription.update_status()
                success_count += 1
                
        if success_count > 0:
            reply_message = f"✅ I have successfully uploaded {success_count} prescription(s), extracted the details, and set up your medicine schedule!"
        else:
            reply_message = "⚠️ I uploaded the document(s), but I couldn't read the details automatically. You might need to update them manually."
            
        return Response({
            "success": True,
            "reply": reply_message,
            "session_id": session_id or 0,
            "intent": "upload_prescription",
            "action": None,
            "data": {},
            "action_executed": True
        })
    # ---------------------------------------------------------

    response_data = ChatbotEngine.process(
        user=user,
        message=message,
        session_id=session_id,
    )

    response_serializer = ChatResponseSerializer(data=response_data)
    if not response_serializer.is_valid():
        logger.error(f"Chat response serialization failed: {response_serializer.errors}")
        return Response(
            {
                "success": False,
                "error": "Unable to build chatbot response",
                "details": response_serializer.errors,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {
            "success": True,
            **response_serializer.validated_data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def available_tools_view(request):
    try:
        category = request.query_params.get("category")
        tools = ToolRouter.get_available_tools(category)

        return Response(
            {
                "success": True,
                "tools": tools,
                "categories": ToolsRegistry.get_categories(),
            }
        )
    except Exception as e:
        logger.error(f"Error in available_tools_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def tools_description_view(request):
    try:
        summary = ToolsRegistry.get_tools_summary()

        return Response(
            {
                "success": True,
                "tools": summary,
                "total_tools": len(ToolsRegistry.get_all_tools()),
                "categories": ToolsRegistry.get_categories(),
            }
        )
    except Exception as e:
        logger.error(f"Error in tools_description_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

