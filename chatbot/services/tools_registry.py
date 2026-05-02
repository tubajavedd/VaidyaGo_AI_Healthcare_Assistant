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
            "slot": {"type": "integer", "description": "ID of the available time slot (MUST get slots first using get_doctor_slots action)", "required": True},
            "patient_name": {"type": "string", "description": "Name of the patient (auto-filled from user profile if not provided)", "required": False},
            "patient_phone": {"type": "string", "description": "Phone number of the patient (auto-filled from user profile if not provided)", "required": False},
            "user": {"type": "integer", "description": "User ID", "required": False},
            "doctor_id": {"type": "integer", "description": "ID of the doctor (used to get slots)", "required": False},
            "doctor_name": {"type": "string", "description": "Name of the doctor (e.g., Dr. Smith) - used to get available slots", "required": False},
            "date": {"type": "string", "description": "Appointment date (YYYY-MM-DD or day name like 'monday') - used to get slots", "required": False},
            "time": {"type": "string", "description": "Appointment time (HH:MM format) - used to select from available slots", "required": False}
        },
        "notes": "IMPORTANT: You MUST first use 'get_doctor_slots' to get available slots, then use the slot ID from the response to book. Patient info is auto-filled from user profile if available.",
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

    "generate_slots": {
        "name": "generate_slots",
        "description": "Generate appointment slots for a doctor",
        "category": "doctor_slots",
        "endpoint": "/api/generate-slots/",
        "method": "POST",
        "parameters": {
            "doctor_id": {"type": "integer", "description": "ID of the doctor"},
            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "slot_duration": {"type": "integer", "description": "Slot duration in minutes"}
        },
        "response_format": {
            "success": True,
            "message": "Slots generated",
            "total_slots": "integer"
        }
    },

    "upload_doctor_documents": {
        "name": "upload_doctor_documents",
        "description": "Upload medical documents for a doctor",
        "category": "documents",
        "endpoint": "/api/doctor-documents/upload/",
        "method": "POST",
        "parameters": {
            "document_type": {"type": "string", "description": "Type of document (license, certificate, etc.)"},
            "file": {"type": "file", "description": "Document file"}
        },
        "response_format": {
            "success": True,
            "document_id": "integer"
        }
    },

    "get_doctor_documents": {
        "name": "get_doctor_documents",
        "description": "Get all doctor documents",
        "category": "documents",
        "endpoint": "/api/doctor-documents/list/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "documents": [
                {
                    "id": "integer",
                    "type": "string",
                    "filename": "string",
                    "uploaded_at": "datetime"
                }
            ]
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
        "description": "Set a reminder for medication or appointment",
        "category": "reminders",
        "endpoint": "/reminder/set/",
        "method": "POST",
        "parameters": {
            "type": {"type": "string", "description": "Reminder type (medication/appointment)"},
            "title": {"type": "string", "description": "Reminder title"},
            "datetime": {"type": "datetime", "description": "Reminder date and time"},
            "description": {"type": "string", "description": "Reminder description"}
        },
        "response_format": {
            "success": True,
            "reminder_id": "integer"
        }
    },

    "get_reminders": {
        "name": "get_reminders",
        "description": "Get all active reminders",
        "category": "reminders",
        "endpoint": "/reminder/list/",
        "method": "GET",
        "parameters": {},
        "response_format": {
            "reminders": [
                {
                    "id": "integer",
                    "title": "string",
                    "datetime": "datetime",
                    "type": "string"
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

    "update_user_profile": {
        "name": "update_user_profile",
        "description": "Update user profile information",
        "category": "profile",
        "endpoint": "/auth/profile/update/",
        "method": "POST",
        "parameters": {
            "name": {"type": "string", "description": "Full name"},
            "phone": {"type": "string", "description": "Phone number"},
            "age": {"type": "integer", "description": "Age"},
            "address": {"type": "string", "description": "Address"}
        },
        "response_format": {
            "success": True,
            "message": "Profile updated"
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
