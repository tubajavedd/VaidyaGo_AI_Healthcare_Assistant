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
            
            # --- NEW: Check for Voice Cloning Request ---
            cloning_triggers = ["use my voice", "clone my voice", "meri voice use karo", "meri awaaz use karo", "my voice as ai"]
            if any(trigger in message.lower() for trigger in cloning_triggers):
                import shutil
                from django.conf import settings
                
                voice_clone_dir = os.path.join(settings.MEDIA_ROOT, 'voice_clones')
                if not os.path.exists(voice_clone_dir):
                    os.makedirs(voice_clone_dir, exist_ok=True)
                
                # Save as myvoice.wav.m4a as specifically requested
                ref_path = os.path.join(voice_clone_dir, 'myvoice.wav.m4a')
                
                # Seek to beginning in case it was read during transcription
                audio_file.seek(0)
                with open(ref_path, 'wb+') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)
                
                logger.info(f"Voice cloning reference saved to: {ref_path}")
                # We'll continue the chat to confirm it

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
                
                # --- NEW: Vitals Integration ---
                vitals_data = extracted_data.get('vitals')
                if vitals_data:
                    import re
                    def ext_num(v):
                        if not v: return None
                        m = re.search(r'\d+(\.\d+)?', str(v))
                        return float(m.group()) if m else None
                    
                    temp = ext_num(vitals_data.get('temperature_f'))
                    hr = ext_num(vitals_data.get('heart_rate_bpm'))
                    
                    if temp or hr:
                        try:
                            from SymptomChecker.models import Patient as SymptomPatient, DailySymptomVitals
                            symptom_patient = SymptomPatient.objects.filter(name__icontains=user.username).first()
                            if not symptom_patient:
                                symptom_patient = SymptomPatient.objects.create(
                                    patient_id=f"PX-{user.id:04d}",
                                    name=user.username,
                                    age=getattr(user, 'age', 25) or 25
                                )
                            
                            DailySymptomVitals.objects.create(
                                patient=symptom_patient,
                                temperature_f=temp or 98.6,
                                heart_rate_bpm=int(hr) if hr else 72,
                                headache_duration="None",
                                headache_severity="Mild",
                                fatigue_duration="None",
                                fatigue_severity="Mild",
                                eye_strain_duration="None",
                                eye_strain_severity="Mild"
                            )
                        except Exception as e:
                            logger.error(f"Failed to integrate vitals from prescription: {e}")
                            
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

    # Add Natural Voice URL
    from .services.tts_service import TTSService
    try:
        response_data['audio_url'] = TTSService.generate_speech(response_data.get('reply', ''))
    except Exception as tts_err:
        logger.error(f"TTS Generation Error: {str(tts_err)}")
        response_data['audio_url'] = None

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
                prescription.document_type = extracted_data.get('document_type', 'Medical Document')
                prescription.document_name = extracted_data.get('document_name') or extracted_data.get('document_type', 'Medical Document')
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


@api_view(["GET"])
def chat_sessions_api(request):
    """Return real chat session history for the authenticated user, grouped by date."""
    from .models import ChatSession, ChatMessage
    from django.utils import timezone
    from datetime import date

    user = request.user if request.user and request.user.is_authenticated else None
    if not user:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    today = date.today()
    sessions = ChatSession.objects.filter(user=user).order_by("-created_at")[:30]

    sessions_data = []
    for session in sessions:
        # Get the first user message and first AI message to build title/snippet
        first_user_msg = ChatMessage.objects.filter(session=session, sender="user").order_by("created_at").first()
        first_ai_msg = ChatMessage.objects.filter(session=session, sender="assistant").order_by("created_at").first()

        title = (first_user_msg.content[:40] + "...") if first_user_msg and len(first_user_msg.content) > 40 else (first_user_msg.content if first_user_msg else "New Conversation")
        snippet = (first_ai_msg.content[:80] + "...") if first_ai_msg and len(first_ai_msg.content) > 80 else (first_ai_msg.content if first_ai_msg else "")

        session_date = session.created_at.date() if timezone.is_aware(session.created_at) else session.created_at.date()
        if session_date == today:
            group = "Today"
        elif (today - session_date).days == 1:
            group = "Yesterday"
        else:
            group = session_date.strftime("%b %d")

        sessions_data.append({
            "id": session.id,
            "title": title,
            "snippet": snippet,
            "time": session.created_at.strftime("%I:%M %p"),
            "group": group,
        })

    return Response({"success": True, "sessions": sessions_data})
