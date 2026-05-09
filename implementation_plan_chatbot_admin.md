# Implementation Plan - Admin Chatbot Intelligence Feeding

Feed comprehensive platform management information, example queries, and specific intents into the `chatbot_admin` module to enhance its capabilities for platform administrators.

## User Review Required

> [!IMPORTANT]
> The admin chatbot will now have expanded knowledge about platform operations, doctor/patient management, revenue analytics, and system health. Ensure that the AI responses are properly gated by the 'ADMIN' role in the backend (which is already implemented in `ToolRouter`).

## Proposed Changes

### [Component] Chatbot Admin Services

#### [MODIFY] [prompt_service.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_admin/services/prompt_service.py)
- Update `SYSTEM_PROMPT` with the comprehensive knowledge base provided by the user.
- Include categories: Greetings, Dashboard Summary, Doctor Management, Patient Management, Appointment Management, Slot Management, Revenue/Finance, User Analytics, Notifications, Support Tickets, System Health, Security, Reports, Maintenance, Content Moderation, and AI Analytics.

#### [MODIFY] [intent_service.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_admin/services/intent_service.py)
- Expand the `Available Actions` list in the intent extraction system prompt to include all new core intents:
    - `dashboard_summary`
    - `doctor_management`
    - `doctor_approval`
    - `patient_management`
    - `appointments_management`
    - `slot_management`
    - `revenue_analytics`
    - `user_analytics`
    - `notifications`
    - `broadcast`
    - `support_tickets`
    - `system_health`
    - `security`
    - `reports`
    - `maintenance`
    - `logs`
    - `ai_analytics`

#### [MODIFY] [tool_router.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_admin/services/tool_router.py)
- Add handlers for the new intents.
- Implement basic logic for newly added data-driven intents (e.g., `user_analytics`, `revenue_analytics`) using existing models where possible, or provide structured informative responses.

## Verification Plan

### Manual Verification
- Log in as Admin and interact with the chatbot using the example queries provided:
    - "Show dashboard summary"
    - "Show pending doctors"
    - "Top booked doctors"
    - "Monthly revenue"
    - "System health"
- Verify that the chatbot identifies the correct intent and provides a professional, data-oriented response.
- Verify that the chatbot correctly identifies itself as 'Vado SuperAdmin'.
