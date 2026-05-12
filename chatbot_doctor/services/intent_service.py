import json
import logging
from chatbot_doctor.services.mistral_service import MistralService

logger = logging.getLogger(__name__)

class IntentService:
    @staticmethod
    def parse(llm_output):
        """
        Parses the LLM output into an intent and action.
        Expected format: {"intent": "...", "action": "...", "message": "...", "data": {...}}
        """
        try:
            # If the LLM output is already a JSON string
            if llm_output.strip().startswith("{"):
                return json.loads(llm_output)
            
            # If it's just plain text, wrap it as a chat intent
            return {
                "intent": "chat",
                "action": None,
                "message": llm_output,
                "data": {},
                "confidence": 1.0
            }
        except Exception as e:
            logger.error(f"Intent parsing error: {str(e)}")
            return {
                "intent": "chat",
                "action": None,
                "message": llm_output,
                "data": {},
                "confidence": 0.0
            }

    @staticmethod
    def extract_intent_with_llm(message, history):
        """
        Use LLM to explicitly extract intent and data for complex requests.
        """
        system_prompt = """
        You are an advanced medical admin intent extractor for the VaidyaGo chatbot.
        Analyze the doctor's natural language message and return a JSON object mapping to the correct action.

        Categories & Examples to map to Available Actions:
        1. Schedule Management ("Show tomorrow appointments", "Am I free tomorrow?", "Busy hours today"): Map to `get_my_slots` or `get_my_appointments`.
        2. Appointment Management ("List all appointments", "Pending appointments", "Next patient details"): Map to `get_my_appointments`.
        3. Slot Management ("Generate slots for next week", "Block tomorrow slots", "book me today slot", "Open my schedule for Monday"): Map to `generate_slots`.
        4. Patient Management ("Patient list", "Repeat patients", "Who is my next patient?"): Map to `get_my_appointments`.
        5. Appointment details ("Appointment at 10 AM", "Who booked 3 PM?", "Show details for appt 5"): Map to `get_appointment_details`.
        6. Booking/New Appointment ("Book appointment for John", "New booking for Rahul on slot 10", "Make appointment"): Map to `create_appointment`.
        7. Reminder Management ("Add reminder", "Remind me to call patient at 6 PM"): Map to `remind_appointments`.
        8. Reschedule Management ("Move appointment 123 to tomorrow", "Reschedule my 10 AM"): Map to `reschedule_appointment`.
        9. Appointment Specifics ("Show details for appointment 5", "Who is patient in appt 10?"): Map to `get_appointment_details`.
        10. Profile/Registration Info ("Update clinic timing", "My qualifications"): Map to `update_hospital_info` or `get_doctor_profile`.
        11. Casual / Non-Actionable ("Hi", "Good morning", "Thanks"): Map to `chat` with action `null`.
 
        Available Actions:
        - get_my_slots (params: date)
        - generate_slots (params: start_date, end_date, slot_duration, date)
        - get_my_appointments (params: date)
        - get_appointment_details (params: appointment_id)
        - create_appointment (params: slot_id, patient_name, patient_phone, patient_email, appointment_type)
        - get_doctor_profile (params: none)
        - get_professional_info (params: none)
        - get_hospital_info (params: none)
        - list_doctor_documents (params: none)
        - accept_appointment (params: appointment_id, location, appointment_type)
        - reject_appointment (params: appointment_id, reason)
        - cancel_appointment (params: appointment_id, reason)
        - reschedule_appointment (params: appointment_id, slot_id, reason)
        - get_notifications (params: unread_only)
        - update_doctor_profile (params: city, mobile_number, gender)
        - update_professional_info (params: specialization, years_of_experience, department)
        - update_hospital_info (params: consultation_fees, leave_day, employment_type)
        - remind_appointments (params: none)
        - chat (no action, for casual conversation)

        LANGUAGE RULES:
        Detect the language the user is using. If the user speaks in Hindi, or asks you to speak in Hindi, you MUST reply in Hindi using Hinglish (Hindi written in the English alphabet, e.g., "Namaste, aap kaise hain?") in the "message" field. Do NOT use the Devanagari script.

        Return strictly in this format: {"intent": "action_name_or_chat", "action": "action_name_or_null", "message": "conversational response acknowledging the action or chatting", "data": {}}
        """
        prompt = f"History: {history}\nMessage: {message}"
        response = MistralService.generate_raw_response(prompt, system_prompt)
        if response:
            return IntentService.parse(response)
        return {"intent": "chat", "action": None, "message": "I'm not sure how to help with that specifically.", "data": {}}
