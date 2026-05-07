# VaidyaGo Chatbot AI - Complete API Integration Guide

## 🎯 Overview

The VaidyaGo chatbot (Vado AI) is now fully integrated with all available APIs and supports smart document uploads with automatic extraction. This guide explains all features and how to use them.

---

## 📋 Key Features

### 1. **Unified API Access**
- Vado AI can access and call **40+ APIs** across all VaidyaGo modules
- APIs organized by category (appointments, medications, prescriptions, payments, etc.)
- Automatic API selection based on user intent

### 2. **Document Upload & Auto-Extraction**
- Upload medical prescriptions, lab reports, scans, discharge summaries
- Automatic OCR extraction of:
  - Doctor name and hospital information
  - Medicine details (name, dosage, frequency, duration)
  - Test results and findings
  - Recommendations and special instructions
- Automatic medicine schedule creation

### 3. **Smart Prescription Management**
- View all uploaded prescriptions
- Extract detailed information from documents
- Get medicine lists with dosage information
- Track test results and findings
- View doctor and hospital details

---

## 🔧 API Endpoints

### A. Chat & Document Upload

#### 1. **Send Chat Message with Optional Document**
```
POST /api/chatbot/chat/
Content-Type: application/json (or multipart/form-data for files)

{
    "message": "I have a prescription, can you help me understand it?",
    "session_id": 123,
    "document": <file> (optional)
}

Response:
{
    "success": true,
    "reply": "I'll help you! Let me extract the details...",
    "session_id": 123,
    "intent": "upload_prescription",
    "action": null,
    "data": {}
}
```

#### 2. **Upload Prescription via Dedicated Endpoint**
```
POST /api/chatbot/upload-prescription/
Content-Type: multipart/form-data

Parameters:
- document: <medical_document_file>

Response:
{
    "success": true,
    "prescriptions": [
        {
            "prescription_id": 1,
            "document_type": "prescription",
            "doctor_name": "Dr. Smith",
            "hospital_name": "City Hospital",
            "patient_name": "John Doe",
            "medicines": [
                {
                    "name": "Aspirin",
                    "dosage": "500mg",
                    "frequency": "Twice Daily",
                    "duration_days": 7,
                    "instructions": "Take with food"
                }
            ],
            "test_results": [],
            "findings": [],
            "recommendations": [],
            "status": "success"
        }
    ],
    "count": 1
}
```

### B. Prescription Management Endpoints

#### 3. **List All Prescriptions**
```
GET /api/chatbot/prescriptions/list/

Response:
{
    "success": true,
    "prescriptions": [
        {
            "id": 1,
            "doctor_name": "Dr. Smith",
            "hospital_name": "City Hospital",
            "status": "active",
            "prescription_date": "2026-05-07",
            "created_at": "2026-05-07T10:00:00Z",
            "medicines_count": 3
        }
    ],
    "count": 1
}
```

#### 4. **Get Prescription Details**
```
GET /api/chatbot/prescriptions/{prescription_id}/details/

Response:
{
    "success": true,
    "prescription": {
        "id": 1,
        "doctor_name": "Dr. Smith",
        "hospital_name": "City Hospital",
        "patient_name": "John Doe",
        "prescription_date": "2026-05-07",
        "medicines": [...],
        "status": "active"
    }
}
```

#### 5. **Get Medicines from Prescription**
```
GET /api/chatbot/prescriptions/{prescription_id}/medicines/

Response:
{
    "success": true,
    "prescription_id": 1,
    "medicines": [
        {
            "id": 1,
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Twice Daily",
            "duration_days": 7,
            "instructions": "Take with food"
        }
    ],
    "count": 1
}
```

### C. API Discovery

#### 6. **Get All Available APIs**
```
GET /api/chatbot/all-apis/

Response:
{
    "success": true,
    "total_apis": 40,
    "categories": [
        "appointments",
        "medications",
        "prescriptions",
        "payments",
        "profile",
        ...
    ],
    "apis_by_category": {
        "appointments": [
            {
                "name": "book_appointment",
                "description": "Book a medical appointment...",
                "endpoint": "/api/appointments/",
                "method": "POST",
                "parameters": {...},
                "response_format": {...}
            }
        ],
        "prescriptions": [
            {
                "name": "upload_prescription_document",
                "description": "Upload a medical prescription...",
                ...
            }
        ]
    }
}
```

#### 7. **Get Tools Summary**
```
GET /api/chatbot/tools-description/

Response:
{
    "success": true,
    "tools": {
        "appointments": [
            {
                "name": "book_appointment",
                "description": "Book a medical appointment with a doctor"
            }
        ],
        ...
    },
    "total_tools": 40,
    "categories": [...]
}
```

#### 8. **Get Available Tools (by category)**
```
GET /api/chatbot/tools/?category=appointments

Response:
{
    "success": true,
    "tools": [...],
    "categories": [...]
}
```

---

## 🎤 Chatbot Capabilities

### User Can:

1. **Upload and Extract Documents**
   ```
   User: "I have a prescription, can you help me?"
   [Uploads prescription PDF]
   Vado: "✅ I've extracted your prescription! You have 3 medicines:
          - Aspirin 500mg twice daily for 7 days
          - ..."
   ```

2. **Ask About APIs**
   ```
   User: "What can you do for me?"
   Vado: "I can help you with:
         - Book and manage appointments
         - View prescriptions and medicines
         - Set medication reminders
         - Make payments
         - And much more! What do you need?"
   ```

3. **Get Medicine Information**
   ```
   User: "Tell me about my medicines"
   Vado: "From your prescription, you have:
         - Aspirin 500mg - Take twice daily with food
         - [etc]"
   ```

4. **Book Appointments**
   ```
   User: "I want to book an appointment with Dr. Smith"
   Vado: "Sure! Let me check available slots and book it for you..."
   ```

5. **Manage Reminders**
   ```
   User: "Set a reminder for my medicine"
   Vado: "I'll set up reminders for your medicines at the right times!"
   ```

---

## 📚 Available Tool Categories

The chatbot has access to tools in the following categories:

| Category | Tools | Purpose |
|----------|-------|---------|
| **Appointments** | book, cancel, reschedule, list, get_slots | Manage medical appointments |
| **Medications** | get_prescriptions, request_prescription, add_past_medication, get_schedule | Manage medicines |
| **Prescriptions** | upload_document, get_details, list, extract_medicines, get_lab_results | Handle medical documents |
| **Reminders** | set_reminder, get_reminders | Set medication/appointment reminders |
| **Payments** | make_payment, get_history | Handle payments |
| **Profile** | get_profile, update_profile | Manage user profile |
| **Authentication** | send_otp, verify_otp | Verify user identity |
| **Notifications** | get_notifications, mark_read | View notifications |
| **Documents** | upload_doctor_documents, get_doctor_documents | Manage document uploads |
| **Feedback** | submit_feedback | Provide feedback |

---

## 💻 Implementation Details

### Tool Registry
- **File**: `chatbot/services/tools_registry.py`
- **Contains**: 40+ tool definitions with endpoint, method, parameters
- **Updated**: Added prescription document management tools

### Chatbot Engine
- **File**: `chatbot/services/chatbot_engine.py`
- **Flow**: Message → Prompt Build → LLM → Intent Parse → Action Execute

### LLM Service
- **File**: `chatbot/services/llm_service.py`
- **Backends**: Local TinyLlama → OpenAI → HuggingFace → Fallback
- **Status**: Always functional with multi-backend support

### Intent Service
- **File**: `chatbot/services/intent_service.py`
- **Purpose**: Parse LLM output to extract action and parameters

### Tool Router
- **File**: `chatbot/services/tool_router.py`
- **Purpose**: Execute any registered tool based on intent

---

## 🔌 Integration Flow

```
User Message + Document
         ↓
    Chat View
         ↓
Document Upload (if present)
    ↓         ↓
  [OCR]    [Chat Process]
    ↓         ↓
  Extract ← Tools Registry
    ↓         ↓
Save Data → Tool Router
         ↓
   LLM Response
         ↓
   Return to User
```

---

## 📝 Adding New APIs

To add a new API to the chatbot:

1. **Define in Tools Registry**
   ```python
   # In chatbot/services/tools_registry.py
   "new_api": {
       "name": "new_api",
       "description": "What this API does",
       "category": "category_name",
       "endpoint": "/api/endpoint/",
       "method": "POST",
       "parameters": {
           "param1": {"type": "string", "description": "..."}
       },
       "response_format": {...}
   }
   ```

2. **Create Endpoint** (if needed)
   ```python
   # In appropriate app/views.py
   @api_view(["POST"])
   def new_api_view(request):
       # Implementation
   ```

3. **Add URL Pattern**
   ```python
   # In urls.py
   path("new-api/", new_api_view, name="new_api")
   ```

4. **Update Prompt** (optional)
   - Prompt service automatically includes all tools
   - LLM learns about new API from registry

---

## 🧪 Testing

### Test Document Upload
```bash
curl -X POST http://localhost:8000/api/chatbot/upload-prescription/ \
  -H "Authorization: Bearer TOKEN" \
  -F "document=@prescription.pdf"
```

### Test Chat with Document
```bash
curl -X POST http://localhost:8000/api/chatbot/chat/ \
  -H "Authorization: Bearer TOKEN" \
  -F "message=Help with this prescription" \
  -F "document=@prescription.pdf"
```

### Test API Discovery
```bash
curl http://localhost:8000/api/chatbot/all-apis/
```

---

## ✅ Features Included

- ✅ Unified API registry (40+ tools)
- ✅ Document upload via chatbot
- ✅ Automatic OCR extraction
- ✅ Prescription management
- ✅ Medicine extraction
- ✅ API discovery endpoint
- ✅ Enhanced prompt with API info
- ✅ Multi-file upload support
- ✅ Automatic schedule creation
- ✅ Lab results extraction
- ✅ Doctor info extraction

---

## 🚀 Future Enhancements

- [ ] Voice document upload
- [ ] Real-time medicine reminders
- [ ] Doctor recommendation engine
- [ ] Insurance integration
- [ ] Video consultation booking
- [ ] AI-powered health insights

---

## 📞 Support

For issues or questions about the chatbot integration, check:
- `CHATBOT_INTEGRATION_GUIDE.md` - Original integration docs
- `AUTOGEN_GUIDE.md` - AutoGen configuration
- `chatbot/services/` - Service implementations

---

**Last Updated**: May 7, 2026  
**Version**: 2.0 - Complete API Integration
