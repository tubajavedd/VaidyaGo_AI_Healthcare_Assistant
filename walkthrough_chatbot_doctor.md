# Walkthrough - Chatbot Admin (Doctor AI)

I have successfully implemented the `chatbot_doctor` model, a conversational AI specifically designed for doctors. It follows the requested file structure and provides tools for managing medical practices.

## File Structure Implemented

```text
chatbot_doctor/
├── views.py
├── models.py
├── serializers.py
├── urls.py
│
├── services/
│   ├── chatbot_engine.py
│   ├── intent_service.py
│   ├── language_service.py
│   ├── llm_service.py
│   ├── memory_service.py
│   ├── mistral_service.py
│   ├── prompt_service.py
│   ├── smart_extractor.py
│   ├── tool_router.py
│   ├── tools_registry.py
│   └── rag/ (directory created)
```

## Key Features

1.  **Doctor-Specific Persona**: The chatbot identifies as "Vado Admin" and focuses on practice management.
2.  **Tool Integration**:
    *   **Schedule**: `get_my_slots`, `generate_slots`, `get_my_appointments`.
    *   **Profile**: `get_doctor_profile`, `get_professional_info`, `get_hospital_info`.
    *   **Compliance**: `list_doctor_documents` (View status of licenses and certifications).
3.  **Intelligent Intent Extraction**: Uses Mistral LLM to parse doctor requests into actionable tool calls for any of the above areas.
4.  **Secure Access**: Restricted to users with `DOCTOR` or `ADMIN` roles.
5.  **History Management**: Separate `AdminChatSession` and `AdminChatMessage` models to keep doctor and patient chat histories isolated.

## Verification Results

I verified the implementation using a test script that simulates a doctor's request.

**Test Case: "Show me my schedule"**
- **User**: `admin_javedtuba` (linked to Dr. Myra Khan)
- **Detected Intent**: `view_schedule`
- **Action Triggered**: `get_my_slots`
- **Result**: Successfully queried the database and returned a relevant response.

```text
Assistant Reply: You have no slots scheduled for the selected period.
Intent: view_schedule, Action: get_my_slots
Action Executed: True
```

## How to use
- **Endpoint**: `POST /api/vado-admin/chat/`
- **Payload**: `{"message": "Your message here", "session_id": null}`
- **Authentication**: Requires a valid token for a user with role `DOCTOR` or `ADMIN`.
