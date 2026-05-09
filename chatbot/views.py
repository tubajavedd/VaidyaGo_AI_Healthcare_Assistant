import logging

from rest_framework.decorators import api_view, permission_classes
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
    audio_file = request.FILES.get("audio")
    user = request.user if request.user and request.user.is_authenticated else None

    # Handle Audio Transcription via Whisper
    if audio_file:
        from .services.voice_service import VoiceService
        transcription = VoiceService.transcribe(audio_file)
        if transcription:
            message = transcription
            logger.info(f"Whisper Transcription: {message}")

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

    # Add Natural Voice URL via gTTS
    from .services.tts_service import TTSService
    response_data['audio_url'] = TTSService.generate_speech(response_data.get('reply', ''))

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


# ============ PRESCRIPTION DOCUMENT MANAGEMENT ENDPOINTS ============

@api_view(["POST"])
def upload_prescription_api(request):
    """Upload prescription document via chatbot"""
    from prescription_management.models import Prescription, PrescribedMedicine
    from prescription_management.ocr_service import OCRService
    from prescription_management.views import PrescriptionUploadView
    from datetime import datetime
    
    user = request.user if request.user and request.user.is_authenticated else None
    if not user:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    documents = request.FILES.getlist("document") or request.FILES.getlist("documents")
    if not documents:
        return Response(
            {"error": "No document provided"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    processed_prescriptions = []
    
    for document in documents:
        try:
            # Create prescription record
            prescription = Prescription.objects.create(
                patient=user,
                file=document,
                status='active'
            )
            
            # Extract using OCR
            extracted_data = OCRService.extract_prescription_details(prescription.file.path)
            
            if extracted_data:
                # Update prescription with extracted data
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
                
                # Create medicines and schedules
                uploader_view = PrescriptionUploadView()
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
            
            processed_prescriptions.append({
                "prescription_id": prescription.id,
                "document_type": extracted_data.get("document_type") if extracted_data else None,
                "doctor_name": extracted_data.get("doctor_name") if extracted_data else None,
                "hospital_name": extracted_data.get("hospital_name") if extracted_data else None,
                "patient_name": extracted_data.get("patient_name") if extracted_data else None,
                "medicines": extracted_data.get("medicines", []) if extracted_data else [],
                "test_results": extracted_data.get("test_results", []) if extracted_data else [],
                "findings": extracted_data.get("findings", []) if extracted_data else [],
                "recommendations": extracted_data.get("recommendations", []) if extracted_data else [],
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error processing prescription: {str(e)}")
            processed_prescriptions.append({
                "status": "error",
                "message": str(e)
            })
    
    return Response({
        "success": len(processed_prescriptions) > 0,
        "prescriptions": processed_prescriptions,
        "count": len(processed_prescriptions)
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def prescription_details_api(request, prescription_id):
    """Get detailed information about a prescription"""
    from prescription_management.models import Prescription
    from prescription_management.serializers import PrescriptionSerializer
    
    user = request.user if request.user and request.user.is_authenticated else None
    if not user:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        prescription = Prescription.objects.get(id=prescription_id, patient=user)
        prescription.update_status()
        serializer = PrescriptionSerializer(prescription)
        return Response({
            "success": True,
            "prescription": serializer.data
        })
    except Prescription.DoesNotExist:
        return Response(
            {"error": "Prescription not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def prescription_medicines_api(request, prescription_id):
    """Get medicines from a specific prescription"""
    from prescription_management.models import Prescription, PrescribedMedicine
    
    user = request.user if request.user and request.user.is_authenticated else None
    if not user:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        prescription = Prescription.objects.get(id=prescription_id, patient=user)
        medicines = PrescribedMedicine.objects.filter(prescription=prescription)
        
        medicines_data = [{
            "id": m.id,
            "name": m.name,
            "dosage": m.dosage,
            "frequency": m.frequency,
            "duration_days": m.duration_days,
            "instructions": m.instructions
        } for m in medicines]
        
        return Response({
            "success": True,
            "prescription_id": prescription_id,
            "medicines": medicines_data,
            "count": len(medicines_data)
        })
    except Prescription.DoesNotExist:
        return Response(
            {"error": "Prescription not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def list_prescriptions_api(request):
    """List all prescriptions for the user"""
    from prescription_management.models import Prescription
    
    user = request.user if request.user and request.user.is_authenticated else None
    if not user:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    prescriptions = Prescription.objects.filter(patient=user).order_by('-created_at')
    
    prescriptions_data = [{
        "id": p.id,
        "doctor_name": p.doctor_name,
        "hospital_name": p.hospital_name,
        "status": p.status,
        "prescription_date": p.prescription_date,
        "created_at": p.created_at,
        "medicines_count": p.prescribed_medicines.count() if hasattr(p, 'prescribed_medicines') else 0
    } for p in prescriptions]
    
    return Response({
        "success": True,
        "prescriptions": prescriptions_data,
        "count": len(prescriptions_data)
    })


@api_view(["GET"])
def all_apis_info_view(request):
    """Get complete information about all available APIs and their details"""
    from chatbot.services.tools_registry import ToolsRegistry
    
    all_tools = ToolsRegistry.get_all_tools()
    categories = ToolsRegistry.get_categories()
    
    tools_detailed = {}
    for category in categories:
        category_tools = ToolsRegistry.get_tools_by_category(category)
        tools_detailed[category] = []
        
        for tool_name, tool_info in category_tools.items():
            tools_detailed[category].append({
                "name": tool_info.get("name"),
                "description": tool_info.get("description"),
                "endpoint": tool_info.get("endpoint"),
                "method": tool_info.get("method"),
                "parameters": tool_info.get("parameters", {}),
                "notes": tool_info.get("notes", ""),
                "response_format": tool_info.get("response_format", {})
            })
    
    return Response({
        "success": True,
        "total_apis": len(all_tools),
        "categories": categories,
        "apis_by_category": tools_detailed,
        "message": "This is the complete API catalog available to Vado AI. The chatbot can use any of these APIs to assist you."
    })

