# Implementation Plan - Separate Chatbot Duties

The user wants to clearly separate the duties and behaviors of the three chatbots:
1. `chatbot` -> **Patient**
2. `chatbot_admin` -> **Admin**
3. `chatbot_doctor` -> **Doctor**

## Proposed Changes

### 1. `chatbot` (Patient Assistant)
- **File**: `vaidyaGo/vaidyaGo/chatbot/services/prompt_service.py`
- **Changes**:
    - Remove `DOCTOR_SYSTEM_PROMPT_ADDON` and `ADMIN_SYSTEM_PROMPT_ADDON`.
    - Always include `PATIENT_SYSTEM_PROMPT_ADDON` in the `SYSTEM_PROMPT`.
    - Remove the `user_role` switching logic in `build_prompt`.

### 2. `chatbot_doctor` (Doctor Assistant)
- **File**: `vaidyaGo/vaidyaGo/chatbot_doctor/services/prompt_service.py`
- **Changes**:
    - Update `SYSTEM_PROMPT` to include "INDIAN STYLE" personality and "NATURAL CONVERSATION RULES" from the main chatbot.
    - Focus strictly on doctor duties.

### 3. `chatbot_admin` (Admin Assistant)
- **File**: `vaidyaGo/vaidyaGo/chatbot_admin/services/prompt_service.py`
- **Changes**:
    - Update `SYSTEM_PROMPT` to include rich personality and conversation rules.
    - Focus strictly on platform administration.

## Verification Plan
- I will simulate `build_prompt` calls for each service and check the contents of the generated prompt.
