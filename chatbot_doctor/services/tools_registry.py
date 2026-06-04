"""
Unified Tool Registry for Admin Chatbot
Defines all available APIs/tools that the doctor can access
"""

ADMIN_TOOLS_REGISTRY = {
    "get_my_slots": {
        "name": "get_my_slots",
        "description": "View your scheduled available time slots",
        "category": "doctor_slots",
        "endpoint": "/api/doctor/{doctor_id}/slots/",
        "method": "GET",
        "parameters": {
            "date": {"type": "string", "description": "Date to check slots (YYYY-MM-DD)", "required": False}
        }
    },
    "generate_slots": {
        "name": "generate_slots",
        "description": "Generate automatic appointment slots for a date range",
        "category": "doctor_slots",
        "endpoint": "/api/generate-slots/",
        "method": "POST",
        "parameters": {
            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "from_time": {"type": "string", "description": "Shift start time (HH:MM)"},
            "to_time": {"type": "string", "description": "Shift end time (HH:MM)"},
            "slot_duration": {"type": "integer", "description": "Slot duration in minutes. IMPORTANT: Extract this if specified (e.g., '10 min', '15 mins'). Default is 30 if not mentioned."}
        }
    },
    "get_pending_appointments": {
        "name": "get_pending_appointments",
        "description": "View all pending appointment requests that need your approval",
        "category": "appointments",
        "endpoint": "/api/appointments/pending/",
        "method": "GET",
        "parameters": {}
    },
    "get_recent_patients": {
        "name": "get_recent_patients",
        "description": "View a list of patients you have recently consulted with",
        "category": "patients",
        "endpoint": "/api/appointments/recent/",
        "method": "GET",
        "parameters": {}
    },
    "get_my_appointments": {
        "name": "get_my_appointments",
        "description": "View all your appointments (confirmed, pending, etc.)",
        "category": "appointments",
        "endpoint": "/api/appointments/list/",
        "method": "GET",
        "parameters": {
            "date": {"type": "string", "description": "Filter by date (YYYY-MM-DD)", "required": False},
            "status": {"type": "string", "description": "Filter by status (confirmed, pending, cancelled)", "required": False}
        }
    },
    "get_doctor_profile": {
        "name": "get_doctor_profile",
        "description": "View your professional profile details",
        "category": "profile",
        "endpoint": "/api/doctor/profile/",
        "method": "GET",
        "parameters": {}
    },
    "get_professional_info": {
        "name": "get_professional_info",
        "description": "Get your professional background and qualifications",
        "category": "profile",
        "endpoint": "/api/doctor/{doctor_id}/professional-info/",
        "method": "GET",
        "parameters": {}
    },
    "get_hospital_info": {
        "name": "get_hospital_info",
        "description": "Get information about the hospital you are associated with",
        "category": "profile",
        "endpoint": "/api/doctor/{doctor_id}/hospital-info/",
        "method": "GET",
        "parameters": {}
    },
    "list_doctor_documents": {
        "name": "list_doctor_documents",
        "description": "List all uploaded medical documents and licenses",
        "category": "documents",
        "endpoint": "/api/doctor/{doctor_id}/documents/list/",
        "method": "GET",
        "parameters": {}
    },
    "accept_appointment": {
        "name": "accept_appointment",
        "description": "Accept a patient's appointment request",
        "category": "appointments",
        "endpoint": "/api/appointments/accept/{appointment_id}/",
        "method": "PATCH",
        "parameters": {
            "appointment_id": "integer",
            "location": "string",
            "appointment_type": "string"
        }
    },
    "reject_appointment": {
        "name": "reject_appointment",
        "description": "Reject a patient's appointment request",
        "category": "appointments",
        "endpoint": "/api/appointments/reject/{appointment_id}/",
        "method": "PATCH",
        "parameters": {
            "appointment_id": "integer",
            "reason": "string"
        }
    },
    "cancel_appointment": {
        "name": "cancel_appointment",
        "description": "Cancel an already confirmed appointment",
        "category": "appointments",
        "endpoint": "/api/appointments/cancel/{appointment_id}/",
        "method": "PATCH",
        "parameters": {
            "appointment_id": "integer",
            "reason": "string"
        }
    },
    "reschedule_appointment": {
        "name": "reschedule_appointment",
        "description": "Change the time and date of an appointment",
        "category": "appointments",
        "endpoint": "/api/appointments/reschedule/{appointment_id}/",
        "method": "PATCH",
        "parameters": {
            "appointment_id": "integer",
            "slot_id": "integer",
            "reason": "string"
        }
    },
    "get_appointment_details": {
        "name": "get_appointment_details",
        "description": "Get full details about a specific appointment",
        "category": "appointments",
        "endpoint": "/api/appointments/{appointment_id}/",
        "method": "GET",
        "parameters": {
            "appointment_id": "integer"
        }
    },
    "create_appointment": {
        "name": "create_appointment",
        "description": "Book a new appointment for a patient manually",
        "category": "appointments",
        "endpoint": "/api/appointments/",
        "method": "POST",
        "parameters": {
            "slot_id": "integer",
            "patient_name": "string",
            "patient_phone": "string",
            "patient_email": "string",
            "appointment_type": "string"
        }
    },
    "get_notifications": {
        "name": "get_notifications",
        "description": "View your recent notifications",
        "category": "notifications",
        "endpoint": "/api/notifications/",
        "method": "GET",
        "parameters": {
            "unread_only": "boolean"
        }
    },
    "update_doctor_profile": {
        "name": "update_doctor_profile",
        "description": "Update your personal profile details (city, mobile, etc.)",
        "category": "profile",
        "endpoint": "/api/doctor/profile/update/",
        "method": "PATCH",
        "parameters": {
            "city": "string",
            "mobile_number": "string",
            "gender": "string"
        }
    },
    "update_professional_info": {
        "name": "update_professional_info",
        "description": "Update your professional details (specialization, experience, etc.)",
        "category": "profile",
        "endpoint": "/api/doctor/professional-info/update/",
        "method": "PATCH",
        "parameters": {
            "specialization": "string",
            "years_of_experience": "integer",
            "department": "string"
        }
    },
    "update_hospital_info": {
        "name": "update_hospital_info",
        "description": "Update your hospital/employment details (fees, leave day, etc.)",
        "category": "profile",
        "endpoint": "/api/doctor/hospital-info/update/",
        "method": "PATCH",
        "parameters": {
            "consultation_fees": "number",
            "leave_day": "string",
            "employment_type": "string"
        }
    },
    "remind_appointments": {
        "name": "remind_appointments",
        "description": "Send a reminder of today's appointments to your email and app",
        "category": "appointments",
        "endpoint": "/api/doctor/remind-appointments/",
        "method": "POST",
        "parameters": {}
    },
    "submit_for_approval": {
        "name": "submit_for_approval",
        "description": "Submit your profile and documents for final administrator approval",
        "category": "onboarding",
        "endpoint": "/api/submit/{doctor_id}/",
        "method": "POST",
        "parameters": {}
    },
    "delete_slot": {
        "name": "delete_slot",
        "description": "Delete a specific time slot by slot_id or by date and start time.",
        "category": "doctor_slots",
        "endpoint": "/api/doctor/{doctor_id}/slots/delete/",
        "method": "DELETE",
        "parameters": {
            "slot_id": {"type": "integer", "description": "ID of the slot to delete", "required": False},
            "date": {"type": "string", "description": "Date of the slot to delete (YYYY-MM-DD)", "required": False},
            "start_time": {"type": "string", "description": "Start time of the slot to delete (HH:MM or 10:00 AM)", "required": False}
        }
    },
    "delete_all_slots": {
        "name": "delete_all_slots",
        "description": "Delete all slots for the doctor, or all slots on a specific date.",
        "category": "doctor_slots",
        "endpoint": "/api/doctor/{doctor_id}/slots/delete-all/",
        "method": "DELETE",
        "parameters": {
            "date": {"type": "string", "description": "If provided, delete all slots on this date only", "required": False},
            "all": {"type": "boolean", "description": "Set to true to delete all slots", "required": False}
        }
    }
}

class ToolsRegistry:
    @staticmethod
    def get_all_tools():
        return ADMIN_TOOLS_REGISTRY

    @staticmethod
    def get_tool(name):
        return ADMIN_TOOLS_REGISTRY.get(name)

    @staticmethod
    def get_categories():
        return sorted(list(set(t["category"] for t in ADMIN_TOOLS_REGISTRY.values())))
