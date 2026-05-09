# Implementation Plan - Chatbot Admin (Doctor AI)

The goal is to create a new AI model/endpoint in the backend named `chatbot_doctor`. This will be a conversational AI specifically for doctors, allowing them to manage their schedules, create slots, and perform other administrative tasks through a chat interface. It will follow the architecture of the existing patient `chatbot`.

## User Review Required

> [!IMPORTANT]
> The `chatbot_doctor` will be accessible to authenticated users with doctor/admin privileges. I will need to ensure that only doctors can access their own data via this chatbot.

## Proposed Changes

### Core Configuration

#### [MODIFY] [settings.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/vaidyaGo/settings.py)
- Add `chatbot_doctor` to `INSTALLED_APPS`.

### Database Models

#### [MODIFY] [models.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/models.py)
- Define `AdminChatSession` and `AdminChatMessage` models (similar to `chatbot/models.py`).

### Services Layer (Business Logic)

#### [NEW] [tools_registry.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/services/tools_registry.py)
- Define doctor-specific tools:
    - `get_my_slots`: View upcoming slots.
    - `generate_slots`: Generate slots for a specific period.
    - `get_my_appointments`: View appointments booked with the doctor.
    - `update_doctor_profile`: Update professional or personal info.
    - `get_patient_details`: View details of a patient (if relevant).

#### [NEW] [agent_manager.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/services/agent_manager.py)
- Logic to execute the tools defined in the registry by calling the respective internal APIs or models.

#### [NEW] [prompt_service.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/services/prompt_service.py)
- Define a system prompt that sets the persona as a "Doctor's Administrative Assistant".

#### [NEW] [chatbot_engine.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/services/chatbot_engine.py)
- Orchestrator for the admin chatbot, similar to `chatbot/services/chatbot_engine.py`.

#### [NEW] [intent_service.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/services/intent_service.py)
- LLM-based intent parsing for doctor-specific actions.

### API Layer

#### [NEW] [serializers.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/serializers.py)
- Request and response serializers for the chat endpoint.

#### [MODIFY] [views.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/views.py)
- Implement `admin_chat_view` to handle POST requests from doctors.
- Implement tools discovery views.

#### [NEW] [urls.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_doctor/urls.py)
- Register the new views.

#### [MODIFY] [urls.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/vaidyaGo/urls.py)
- Include `chatbot_doctor.urls`.

## Verification Plan

### Automated Tests
- Create a test script `test_chatbot_doctor.py` to:
    - Test authenticated access (doctor).
    - Test basic conversation.
    - Test tool triggering (e.g., "Show my schedule").
    - Test slot generation via chat (e.g., "Generate slots for next week").

### Manual Verification
- Verify the responses via API testing tools (Postman/Curl).
- Check if the database records for `AdminChatSession` and `AdminChatMessage` are created correctly.
