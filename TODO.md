# TODO: Auto-fill Missing Information for Appointment Booking

## Problem
When user says "Book an appointment with Dr. Smith on Monday at 10 AM", the chatbot cannot complete booking because it's missing:
1. `slot` (the TimeSlot ID) - needs to be looked up from doctor + date + time
2. `patient_name`, `patient_phone` - could come from authenticated user's profile

## Solution Plan - COMPLETED

### Step 1: Modify ToolRouter to auto-fill patient info from user profile ✅
- When executing book_appointment and patient_name/patient_phone are missing
- Check if user is authenticated and fetch their profile info
- Auto-fill patient_name and patient_phone from profile
- Implemented: ToolRouter._auto_fill_patient_info()

### Step 2: Modify ToolRouter to auto-resolve slot ID ✅
- When slot ID is missing but doctor name + date + time are provided
- Call get_doctor_slots to find matching slot
- Extract slot ID from the response
- Implemented: ToolRouter._auto_resolve_slot() and ToolRouter._resolve_doctor_id()

### Step 3: Update tools_registry.py ✅
- Make patient_name and patient_phone optional (handled by ToolRouter)
- Add doctor_name, date, time as optional parameters to help resolve slot

### Step 4: Update prompt_service.py ✅
- Inform LLM about auto-fill capabilities
- Tell LLM to extract doctor name, day name, time from message

## Implementation Files
- chatbot/services/tool_router.py - Main logic changes (COMPLETED)
- chatbot/services/tools_registry.py - Parameter updates (COMPLETED)
- chatbot/services/prompt_service.py - LLM instructions (COMPLETED)

## Follow-up Steps
- Test the chatbot with "Book an appointment with Dr. Smith on Monday at 10 AM"
- Verify patient info is auto-filled from user profile
- Verify slot ID is auto-resolved
