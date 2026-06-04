"""
Unified Tool Registry for Chatbot
Defines all available APIs/tools that the chatbot can access
"""

TOOLS_REGISTRY = {
"book_appointment": {
        "name": "book_appointment",
        "description": "Book a medical appointment with a doctor",
        "category": "appointments",
        "endpoint": "/api/appointments/",
        "method": "POST",
        "parameters": {
            "slot": {"type": "integer", "description": "ID of the available time slot (optional if date and time are provided)", "required": False},
            "patient_name": {"type": "string", "description": "Name of the patient (auto-filled from user profile if not provided)", "required": False},
            "patient_phone": {"type": "string", "description": "Phone number of the patient (auto-filled from user profile if not provided)", "required": False},
            "user": {"type": "integer", "description": "User ID", "required": False},
            "doctor_id": {"type": "integer", "description": "ID of the doctor", "required": False},
            "doctor_name": {"type": "string", "description": "Name of the doctor (e.g., Dr. Smith)", "required": False},
            "date": {"type": "string", "description": "Appointment date (YYYY-MM-DD or day name like 'monday')", "required": False},
            "time": {"type": "string", "description": "Appointment time (HH:MM format)", "required": False}
        },
        "notes": "You can book an appointment directly by providing doctor_name, date, and time. If you don't have the exact time, use 'get_doctor_slots' first. Patient info is auto-filled from user profile.",
        "response_format": {
            "success": True,
            "message": "Appointment booked",
            "id": "integer"
        }
    },

    "cancel_appointment": {
        "name": "cancel_appointment",
        "description": "Cancel an existing appointment",
        "category": "appointments",
        "endpoint": "/api/appointments/{appointment_id}/cancel/",
        "method": "PATCH",
        "parameters": {
            "appointment_id": {"type": "integer", "description": "ID of the appointment to cancel (in URL)", "required": True},
            "reason": {"type": "string", "description": "Reason for cancellation", "required": False}
        },
        "response_format": {
            "success": True,
            "message": "Appointment cancelled"
        }
    },

    "reschedule_appointment": {
        "name": "reschedule_appointment",
        "description": "Reschedule an existing appointment",
        "category": "appointments",
        "endpoint": "/api/appointments/{appointment_id}/reschedule/",
        "method": "POST",
        "parameters": {
            "appointment_id": {"type": "integer", "description": "ID of the appointment (in URL)", "required": True},
            "new_date": {"type": "string", "description": "New appointment date (YYYY-MM-DD)", "required": True},
            "new_time": {"type": "string", "description": "New appointment time (HH:MM)", "required": True}
        },
        "response_format": {
            "success": True,
            "message": "Appointment rescheduled"
        }
    },

    "list_appointments": {
        "name": "list_appointments",
        "description": "Get list of all user appointments",
        "category": "appointments",
        "endpoint": "/api/appointments/list/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "appointments": [
                {
                    "id": "integer",
                    "doctor": "string",
                    "date": "string",
                    "time": "string",
                    "status": "string"
                }
            ]
        }
    },

    "get_doctor_slots": {
        "name": "get_doctor_slots",
        "description": "Get available time slots for a doctor",
        "category": "doctor_slots",
        "endpoint": "/api/doctor/{doctor_id}/slots/",
        "method": "GET",
        "parameters": {
            "doctor_id": {"type": "integer", "description": "ID of the doctor", "required": True},
            "date": {"type": "string", "description": "Date to check slots (YYYY-MM-DD)", "required": False}
        },
        "response_format": {
            "available_slots": ["10:00", "10:30", "11:00"]
        }
    },



    "submit_feedback": {
        "name": "submit_feedback",
        "description": "Submit feedback about a doctor or appointment",
        "category": "feedback",
        "endpoint": "/api/feedback/submit/",
        "method": "POST",
        "parameters": {
            "doctor_id": {"type": "integer", "description": "ID of the doctor"},
            "appointment_id": {"type": "integer", "description": "ID of the appointment"},
            "rating": {"type": "integer", "description": "Rating from 1 to 5"},
            "comment": {"type": "string", "description": "Feedback comment"}
        },
        "response_format": {
            "success": True,
            "message": "Feedback submitted"
        }
    },

    "get_prescriptions": {
        "name": "get_prescriptions",
        "description": "Get active prescriptions for the user",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/active/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "prescriptions": [
                {
                    "id": "integer",
                    "medicine": "string",
                    "dosage": "string",
                    "frequency": "string",
                    "end_date": "string"
                }
            ]
        }
    },

    "request_prescription": {
        "name": "request_prescription",
        "description": "Request a new prescription from a doctor",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/request/",
        "method": "POST",
        "parameters": {
            "doctor_id": {"type": "integer", "description": "ID of the doctor"},
            "medication_name": {"type": "string", "description": "Name of medication"},
            "reason": {"type": "string", "description": "Reason for medication"}
        },
        "response_format": {
            "success": True,
            "request_id": "integer"
        }
    },

    "add_past_medication": {
        "name": "add_past_medication",
        "description": "Add past medication history",
        "category": "medications",
        "endpoint": "/api/medications/past/add/",
        "method": "POST",
        "parameters": {
            "medication_name": {"type": "string", "description": "Name of the medication"},
            "dosage": {"type": "string", "description": "Dosage"},
            "duration": {"type": "string", "description": "Duration taken"},
            "reason": {"type": "string", "description": "Reason for medication"}
        },
        "response_format": {
            "success": True,
            "message": "Medication added to history"
        }
    },

    "get_medication_schedule": {
        "name": "get_medication_schedule",
        "description": "Get today's medication schedule reminders",
        "category": "medications",
        "endpoint": "/today-schedule/reminders/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "medications": [
                {
                    "name": "string",
                    "time": "string",
                    "dosage": "string"
                }
            ]
        }
    },

    "send_otp": {
        "name": "send_otp",
        "description": "Send OTP for verification",
        "category": "authentication",
        "endpoint": "/accounts/send-otp/",
        "method": "POST",
        "parameters": {
            "email": {"type": "string", "description": "Email address"}
        },
        "response_format": {
            "success": True,
            "message": "OTP sent"
        }
    },

    "verify_otp": {
        "name": "verify_otp",
        "description": "Verify OTP code",
        "category": "authentication",
        "endpoint": "/accounts/verify-otp/",
        "method": "POST",
        "parameters": {
            "email": {"type": "string", "description": "Email address"},
            "otp": {"type": "string", "description": "OTP code"}
        },
        "response_format": {
            "success": True,
            "message": "OTP verified"
        }
    },

    "get_notifications": {
        "name": "get_notifications",
        "description": "Get all notifications for the user",
        "category": "notifications",
        "endpoint": "/notifications/list/",
        "method": "GET",
        "parameters": {
            "limit": {"type": "integer", "description": "Number of notifications (default: 10)"}
        },
        "response_format": {
            "notifications": [
                {
                    "id": "integer",
                    "message": "string",
                    "type": "string",
                    "created_at": "datetime"
                }
            ]
        }
    },

    "mark_notification_read": {
        "name": "mark_notification_read",
        "description": "Mark a notification as read",
        "category": "notifications",
        "endpoint": "/notifications/mark-read/",
        "method": "POST",
        "parameters": {
            "notification_id": {"type": "integer", "description": "ID of the notification"}
        },
        "response_format": {
            "success": True,
            "message": "Notification marked as read"
        }
    },

    "set_reminder": {
        "name": "set_reminder",
        "description": "Set a medication reminder for the user (e.g., 'remind me to take Paracetamol 500mg twice a day for 5 days')",
        "category": "reminders",
        "endpoint": "/reminder/create/",
        "method": "POST",
        "parameters": {
            "medicine_name": {"type": "string", "description": "Name of the medicine", "required": True},
            "dosage": {"type": "string", "description": "Dosage (e.g., 500mg, 1 tablet)", "required": False},
            "frequency": {"type": "string", "description": "Frequency (e.g., twice daily, 1-0-1)", "required": False},
            "times": {"type": "array", "items": {"type": "string"}, "description": "Time slots: morning, afternoon, evening, night", "required": False},
            "duration_days": {"type": "integer", "description": "Duration in days", "required": False}
        },
        "response_format": {
            "success": True,
            "message": "Reminder set successfully"
        }
    },

    "get_reminders": {
        "name": "get_reminders",
        "description": "View all active medication reminders and schedules",
        "category": "reminders",
        "endpoint": "/reminder/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "reminders": [
                {
                    "id": "integer",
                    "medicine_name": "string",
                    "dosage": "string",
                    "frequency": "string",
                    "times": "array",
                    "end_date": "string"
                }
            ]
        }
    },

    "make_payment": {
        "name": "make_payment",
        "description": "Make a payment for medical services",
        "category": "payment",
        "endpoint": "/payment/create/",
        "method": "POST",
        "parameters": {
            "amount": {"type": "float", "description": "Amount to pay"},
            "service_type": {"type": "string", "description": "Type of service"},
            "description": {"type": "string", "description": "Payment description"}
        },
        "response_format": {
            "success": True,
            "transaction_id": "string",
            "payment_link": "string"
        }
    },

    "get_payment_history": {
        "name": "get_payment_history",
        "description": "Get payment history",
        "category": "payment",
        "endpoint": "/payment/history/",
        "method": "GET",
        "parameters": {
            "limit": {"type": "integer", "description": "Number of records"}
        },
        "response_format": {
            "payments": [
                {
                    "id": "string",
                    "amount": "float",
                    "status": "string",
                    "date": "datetime"
                }
            ]
        }
    },

    "get_user_profile": {
        "name": "get_user_profile",
        "description": "Get user profile information",
        "category": "profile",
        "endpoint": "/auth/profile/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "user": {
                "id": "integer",
                "name": "string",
                "email": "string",
                "phone": "string",
                "age": "integer"
            }
        }
    },

    "Edit_profile": {
        "name": "Edit_profile",
        "description": "Update user profile information such as name, phone, address, and emergency contact",
        "category": "profile",
        "endpoint": "/profile/edit-profile/",
        "method": "PUT",
        "parameters": {
            "full_name": {"type": "string", "description": "Full name", "required": False},
            "phone_number": {"type": "string", "description": "Phone number", "required": False},
            "email": {"type": "string", "description": "Email address", "required": False},
            "dob": {"type": "string", "description": "Date of birth (YYYY-MM-DD)", "required": False},
            "gender": {"type": "string", "description": "Gender (male, female, other)", "required": False},
            "residential_address": {"type": "string", "description": "Full residential address", "required": False},
            "emergency_contact_name": {"type": "string", "description": "Emergency contact name", "required": False},
            "emergency_contact_number": {"type": "string", "description": "Emergency contact phone number", "required": False}
        },
        "response_format": {
            "success": True,
            "message": "Profile updated successfully"
        }
    },

    "upload_prescription_document": {
        "name": "upload_prescription_document",
        "description": "Upload a medical prescription or document for OCR extraction",
        "category": "prescriptions",
        "endpoint": "/api/chatbot/upload-prescription/",
        "method": "POST",
        "parameters": {
            "document": {"type": "file", "description": "Medical document file (image or PDF)"}
        },
        "response_format": {
            "success": True,
            "prescription_id": "integer",
            "document_type": "string",
            "doctor_name": "string",
            "hospital_name": "string",
            "patient_name": "string",
            "medicines": [
                {
                    "name": "string",
                    "dosage": "string",
                    "frequency": "string",
                    "duration_days": "integer",
                    "instructions": "string"
                }
            ],
            "test_results": [],
            "findings": [],
            "recommendations": []
        }
    },

    "get_prescription_details": {
        "name": "get_prescription_details",
        "description": "Get detailed information about a specific prescription",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/{prescription_id}/details/",
        "method": "GET",
        "parameters": {
            "prescription_id": {"type": "integer", "description": "ID of the prescription"}
        },
        "response_format": {
            "prescription": {
                "id": "integer",
                "doctor_name": "string",
                "hospital_name": "string",
                "patient_name": "string",
                "prescription_date": "string",
                "medicines": "array",
                "status": "string"
            }
        }
    },

    "list_prescription_documents": {
        "name": "list_prescription_documents",
        "description": "Get list of all uploaded prescription documents",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/list/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "prescriptions": [
                {
                    "id": "integer",
                    "doctor_name": "string",
                    "status": "string",
                    "created_at": "datetime",
                    "medicines_count": "integer"
                }
            ]
        }
    },

    "extract_prescription_medicines": {
        "name": "extract_prescription_medicines",
        "description": "Extract and get all medicines from a prescription document",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/{prescription_id}/medicines/",
        "method": "GET",
        "parameters": {
            "prescription_id": {"type": "integer", "description": "ID of the prescription"}
        },
        "response_format": {
            "medicines": [
                {
                    "name": "string",
                    "dosage": "string",
                    "frequency": "string",
                    "duration_days": "integer",
                    "instructions": "string"
                }
            ],
            "total_count": "integer"
        }
    },

    "get_prescription_lab_results": {
        "name": "get_prescription_lab_results",
        "description": "Extract and get lab test results from a medical document",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/{prescription_id}/lab-results/",
        "method": "GET",
        "parameters": {
            "prescription_id": {"type": "integer", "description": "ID of the prescription document"}
        },
        "response_format": {
            "test_results": [
                {
                    "test_name": "string",
                    "result": "string",
                    "unit": "string",
                    "reference_range": "string",
                    "status": "string"
                }
            ]
        }
    },

    "get_doctor_info_from_prescription": {
        "name": "get_doctor_info_from_prescription",
        "description": "Extract doctor and hospital information from a prescription",
        "category": "prescriptions",
        "endpoint": "/api/prescriptions/{prescription_id}/doctor-info/",
        "method": "GET",
        "parameters": {
            "prescription_id": {"type": "integer", "description": "ID of the prescription"}
        },
        "response_format": {
            "doctor_name": "string",
            "hospital_name": "string",
            "doctor_phone": "string",
            "hospital_address": "string"
        }
    },
    "add_symptoms": {
        "name": "add_symptoms",
        "description": "Log patient symptoms and vitals (headache, fatigue, eye strain, temperature, heart rate)",
        "category": "health",
        "parameters": {
            "headache_duration": {"type": "string", "description": "e.g., '2 hours'", "required": False},
            "headache_severity": {"type": "string", "description": "Mild, Moderate, or Severe", "required": False},
            "fatigue_duration": {"type": "string", "description": "e.g., '1 day'", "required": False},
            "fatigue_severity": {"type": "string", "description": "Mild, Moderate, or Severe", "required": False},
            "eye_strain_duration": {"type": "string", "description": "e.g., '30 mins'", "required": False},
            "eye_strain_severity": {"type": "string", "description": "Mild, Moderate, or Severe", "required": False},
            "temperature_f": {"type": "number", "description": "Body temperature in Fahrenheit", "required": False},
            "heart_rate_bpm": {"type": "integer", "description": "Heart rate in beats per minute", "required": False}
        }
    },

    "mark_medication_taken": {
        "name": "mark_medication_taken",
        "description": "Mark a medication reminder or schedule item as taken (dismissed)",
        "category": "medication",
        "parameters": {
            "reminder_id": {"type": "integer", "description": "ID of the reminder/schedule item", "required": True},
            "medication_name": {"type": "string", "description": "Name of the medicine (optional lookup)", "required": False}
        }
    },

    "get_today_schedule": {
        "name": "get_today_schedule",
        "description": "Get all medications scheduled for today",
        "category": "medication",
        "parameters": {}
    },

    "request_refill": {
        "name": "request_refill",
        "description": "Request a refill for an active prescription",
        "category": "medication",
        "parameters": {
            "medication_id": {"type": "integer", "description": "ID of the medication", "required": True},
            "pharmacy_id": {"type": "integer", "description": "ID of the pharmacy", "required": True},
            "delivery_preference": {"type": "string", "description": "pickup or delivery", "required": True}
        }
    },

    "get_notifications": {
        "name": "get_notifications",
        "description": "Get unread notifications and appointment alerts",
        "category": "system",
        "parameters": {
            "limit": {"type": "integer", "description": "Number of notifications to fetch", "required": False}
        }
    }
}


class ToolsRegistry:
    """Registry for managing available tools/APIs"""

    @staticmethod
    def get_all_tools():
        """Get all available tools"""
        return TOOLS_REGISTRY

    @staticmethod
    def get_tools_by_category(category):
        """Get tools filtered by category"""
        return {
            name: tool
            for name, tool in TOOLS_REGISTRY.items()
            if tool.get("category") == category
        }

    @staticmethod
    def get_tool(tool_name):
        """Get specific tool by name"""
        return TOOLS_REGISTRY.get(tool_name)

    @staticmethod
    def get_tool_names():
        """Get list of all available tool names"""
        return list(TOOLS_REGISTRY.keys())

    @staticmethod
    def get_categories():
        """Get all available tool categories"""
        categories = set()
        for tool in TOOLS_REGISTRY.values():
            categories.add(tool.get("category"))
        return sorted(list(categories))

    @staticmethod
    def get_tools_summary():
        """Get formatted summary of all tools"""
        summary = {}
        for category in ToolsRegistry.get_categories():
            tools = ToolsRegistry.get_tools_by_category(category)
            summary[category] = [
                {
                    "name": tool["name"],
                    "description": tool["description"]
                }
                for tool in tools.values()
            ]
        return summary
