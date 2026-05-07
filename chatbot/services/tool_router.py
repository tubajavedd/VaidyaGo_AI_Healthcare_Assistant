import logging
import re
from datetime import datetime, timedelta

from django.db import transaction
from Dr_personalInfo.models import DoctorPersonalInfo
from DoctorSlot.models import TimeSlot
from appointments.models import Appointment

logger = logging.getLogger(__name__)


class ToolRouter:
    """
    Executes actions based on LLM intent output.
    """

    @staticmethod
    def execute(intent_data, user):
        action = intent_data.get("action") or intent_data.get("intent")
        data = intent_data.get("data", {}) or {}
        message = intent_data.get("message", "")

        logger.info(f"ToolRouter received action: {action}")

        if not action or action == "chat":
            return {
                "message": message or "How can I help you today?",
                "action_executed": False,
                "data": {},
            }

        if action == "book_appointment":
            return ToolRouter._book_appointment(data, user)

        if action == "get_doctor_slots":
            return ToolRouter._get_doctor_slots(data)

        if action == "cancel_appointment":
            return ToolRouter._cancel_appointment(data)

        if action == "reschedule_appointment":
            return ToolRouter._reschedule_appointment(data)

        if action == "list_appointments":
            return ToolRouter._list_appointments(user)

        if action == "get_prescriptions":
            return ToolRouter._get_prescriptions(user)

        if action == "get_notifications":
            return {
                "message": "I can show your notifications, but no notifications endpoint is configured yet.",
                "action_executed": False,
                "data": {},
            }

        return {
            "message": message or f"I could not process the action '{action}'.",
            "action_executed": False,
            "data": {},
        }

    @staticmethod
    def _book_appointment(data, user):
        doctor = ToolRouter._resolve_doctor(data.get("doctor_name"), data.get("doctor_id"))
        if not doctor:
            return {
                "message": "I could not find the doctor you requested. Please provide doctor name or ID.",
                "action_executed": False,
                "data": {},
            }

        date_value = ToolRouter._format_date(data.get("date"))
        time_value = ToolRouter._format_time(data.get("time"))

        if not date_value:
            return {
                "message": f"For which date would you like to book the appointment with Dr. {doctor.first_name} {doctor.last_name}?",
                "action_executed": False,
                "data": {"missing_field": "date", "doctor_id": doctor.id},
            }

        if not time_value:
            return {
                "message": f"What time works for you on {date_value}?",
                "action_executed": False,
                "data": {"missing_field": "time", "date": date_value, "doctor_id": doctor.id},
            }

        slot = ToolRouter._find_available_slot(doctor, date_value, time_value)
        if not slot:
            slots = ToolRouter._list_available_slots(doctor, date_value)
            if slots:
                return {
                    "message": (
                        f"I could not find a free slot at {ToolRouter._human_time(time_value)} for Dr. {doctor.last_name}. "
                        f"Available times on {date_value}: {', '.join(slots)}."
                    ),
                    "action_executed": False,
                    "data": {"available_slots": slots},
                }
            return {
                "message": f"No available slots found for Dr. {doctor.last_name} on {date_value}.",
                "action_executed": False,
                "data": {},
            }

        patient_name = data.get("patient_name") or ToolRouter._extract_patient_name(user)
        patient_phone = data.get("patient_phone") or ToolRouter._extract_patient_phone(user)

        if not patient_name:
            return {
                "message": "May I know the patient's name for this booking?",
                "action_executed": False,
                "data": {"missing_field": "patient_name", "date": date_value, "time": time_value, "doctor_id": doctor.id},
            }

        if not patient_phone:
            return {
                "message": "And could you please provide a contact phone number?",
                "action_executed": False,
                "data": {"missing_field": "patient_phone", "date": date_value, "time": time_value, "doctor_id": doctor.id, "patient_name": patient_name},
            }

        try:
            with transaction.atomic():
                # Re-fetch the slot with a lock to prevent race conditions
                locked_slot = TimeSlot.objects.select_for_update().get(id=slot.id)
                
                if locked_slot.is_booked:
                    return {
                        "message": "I'm sorry, that slot was just booked by someone else. Please choose another time.",
                        "action_executed": False,
                        "data": {},
                    }

                appointment = Appointment.objects.create(
                    doctor=doctor,
                    slot=locked_slot,
                    user=user.id if user else None,
                    patient_name=patient_name,
                    patient_phone=patient_phone,
                    start_time=locked_slot.start_time,
                    end_time=locked_slot.end_time,
                    status='booked',
                )
                locked_slot.is_booked = True
                locked_slot.save()

            # Send notification outside the atomic block
            try:
                from appointments.views import notify_appointment_change
                title = "Appointment Booked Successfully"
                msg = (
                    f"Hello {patient_name},\n\n"
                    f"Your appointment with Dr. {doctor.first_name} {doctor.last_name} has been booked for "
                    f"{date_value} at {ToolRouter._human_time(time_value)}.\n\n"
                    f"Thank you for using VaidyaGo!"
                )
                notify_appointment_change(appointment, title, msg)
            except Exception as e:
                logger.warning(f"Failed to send booking notification: {e}")

            return {
                "message": (
                    f"Your appointment with Dr. {doctor.first_name} {doctor.last_name} has been booked for "
                    f"{patient_name} on {date_value} at {ToolRouter._human_time(time_value)}."
                ),
                "action_executed": True,
                "data": {
                    "appointment_id": appointment.id,
                    "doctor_id": doctor.id,
                    "slot_id": locked_slot.id,
                    "patient_name": patient_name,
                    "patient_phone": patient_phone,
                    "date": date_value,
                    "time": time_value
                },
            }
        except Exception as exc:
            logger.error(f"Booking failed: {exc}")
            return {
                "message": f"I could not complete the booking: {exc}",
                "action_executed": False,
                "data": {},
            }

    @staticmethod
    def _get_doctor_slots(data):
        doctor = ToolRouter._resolve_doctor(data.get("doctor_name"), data.get("doctor_id"))
        if not doctor:
            return {
                "message": "Please provide a valid doctor name or ID to fetch available slots.",
                "action_executed": False,
                "data": {},
            }

        date_value = ToolRouter._format_date(data.get("date"))
        slots = ToolRouter._list_available_slots(doctor, date_value)
        if not slots:
            return {
                "message": (
                    f"No available slots were found for Dr. {doctor.first_name} {doctor.last_name} "
                    f"on {date_value or 'the selected date'}."
                ),
                "action_executed": False,
                "data": {},
            }

        human_slots = [ToolRouter._human_time(s) for s in slots]
        date_str = date_value if date_value else "the upcoming days"

        return {
            "message": (
                f"Dr. {doctor.first_name} {doctor.last_name} is available on {date_str} at these times: "
                f"{', '.join(human_slots)}. Which one would you like to book?"
            ),
            "action_executed": False,
            "data": {"available_slots": slots, "doctor_id": doctor.id, "date": date_value},
        }

    @staticmethod
    def _cancel_appointment(data):
        appointment_id = data.get("appointment_id")
        if not appointment_id:
            return {
                "message": "I need the appointment ID to cancel your appointment.",
                "action_executed": False,
                "data": {},
            }

        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.status == "cancelled":
                return {
                    "message": "This appointment has already been cancelled.",
                    "action_executed": False,
                    "data": {},
                }
            appointment.status = "cancelled"
            appointment.save()
            if appointment.slot:
                appointment.slot.is_booked = False
                appointment.slot.save()
            return {
                "message": "Your appointment has been cancelled successfully.",
                "action_executed": True,
                "data": {"appointment_id": appointment_id},
            }
        except Appointment.DoesNotExist:
            return {
                "message": "I could not find that appointment ID.",
                "action_executed": False,
                "data": {},
            }
        except Exception as exc:
            logger.error(f"Cancel appointment error: {exc}")
            return {
                "message": f"Unable to cancel appointment: {exc}",
                "action_executed": False,
                "data": {},
            }

    @staticmethod
    def _reschedule_appointment(data):
        appointment_id = data.get("appointment_id")
        new_date = ToolRouter._format_date(data.get("new_date") or data.get("date"))
        new_time = ToolRouter._format_time(data.get("new_time") or data.get("time"))

        if not appointment_id or not new_date or not new_time:
            return {
                "message": "To reschedule, I need the appointment ID, new date, and new time.",
                "action_executed": False,
                "data": {},
            }

        try:
            appointment = Appointment.objects.get(id=appointment_id)
            doctor = appointment.doctor
            new_slot = ToolRouter._find_available_slot(doctor, new_date, new_time)
            if not new_slot:
                return {
                    "message": "I could not find an available slot for the requested time.",
                    "action_executed": False,
                    "data": {},
                }

            with transaction.atomic():
                if appointment.slot:
                    appointment.slot.is_booked = False
                    appointment.slot.save()

                appointment.slot = new_slot
                appointment.start_time = new_slot.start_time
                appointment.end_time = new_slot.end_time
                appointment.status = "booked"
                appointment.save()
                new_slot.is_booked = True
                new_slot.save()

            return {
                "message": (
                    f"Your appointment has been rescheduled to {new_date} at {ToolRouter._human_time(new_time)}."
                ),
                "action_executed": True,
                "data": {"appointment_id": appointment.id, "slot_id": new_slot.id},
            }
        except Appointment.DoesNotExist:
            return {
                "message": "I could not find that appointment.",
                "action_executed": False,
                "data": {},
            }
        except Exception as exc:
            logger.error(f"Reschedule error: {exc}")
            return {
                "message": f"Unable to reschedule appointment: {exc}",
                "action_executed": False,
                "data": {},
            }

    @staticmethod
    def _list_appointments(user):
        if not user:
            return {
                "message": "Log in to see your appointments.",
                "action_executed": False,
                "data": {},
            }

        appointments = Appointment.objects.filter(user=user.id, status="booked").order_by("start_time")
        appointment_list = [
            {
                "id": appt.id,
                "doctor": f"{appt.doctor.first_name} {appt.doctor.last_name}",
                "date": appt.start_time.strftime("%Y-%m-%d"),
                "time": appt.start_time.strftime("%H:%M"),
                "status": appt.status,
            }
            for appt in appointments
        ]

        return {
            "message": f"You have {len(appointment_list)} upcoming appointment(s).",
            "action_executed": False,
            "data": {"appointments": appointment_list},
        }

    @staticmethod
    def _get_prescriptions(user):
        if not user:
            return {
                "message": "Please log in to view your prescriptions.",
                "action_executed": False,
                "data": {},
            }

        try:
            from prescription_management.models import Prescription
            active_prescriptions = Prescription.objects.filter(patient=user).order_by('-created_at')
            
            if not active_prescriptions.exists():
                return {
                    "message": "You don't have any prescriptions on record.",
                    "action_executed": True,
                    "data": {"prescriptions": []},
                }

            presc_list = []
            structured_data = []
            
            for p in active_prescriptions:
                meds = p.medicines.all()
                if meds.exists():
                    meds_str = ", ".join([f"{m.name} ({m.dosage or 'unknown dosage'})" for m in meds])
                else:
                    meds_str = "No specific medicines parsed."
                    
                date_str = p.prescription_date.strftime("%Y-%m-%d") if p.prescription_date else p.created_at.strftime("%Y-%m-%d")
                presc_list.append(f"- By Dr. {p.doctor_name or 'Unknown'} on {date_str}: {meds_str}")
                
                structured_data.append({
                    "doctor_name": p.doctor_name,
                    "date": date_str,
                    "status": p.status,
                    "medicines": [{"name": m.name, "dosage": m.dosage, "frequency": m.frequency} for m in meds]
                })

            message = "Here are your prescriptions:\n" + "\n".join(presc_list)
            return {
                "message": message,
                "action_executed": True,
                "data": {
                    "prescriptions": structured_data
                }
            }
        except Exception as e:
            logger.error(f"Failed to fetch prescriptions: {e}")
            return {
                "message": "I encountered an error while fetching your prescriptions.",
                "action_executed": False,
                "data": {},
            }

    @staticmethod
    def _resolve_doctor(doctor_name, doctor_id):
        if doctor_id:
            try:
                return DoctorPersonalInfo.objects.get(id=doctor_id)
            except DoctorPersonalInfo.DoesNotExist:
                return None

        if not doctor_name:
            return None

        normalized = re.sub(r"^(dr\.?\s*|doctor\s+)", "", doctor_name.strip(), flags=re.IGNORECASE)
        parts = normalized.split()
        queryset = DoctorPersonalInfo.objects.all()

        if len(parts) == 1:
            return queryset.filter(
                first_name__icontains=parts[0]
            ).first() or queryset.filter(last_name__icontains=parts[0]).first()

        if len(parts) >= 2:
            first, last = parts[0], parts[-1]
            doctor = queryset.filter(
                first_name__icontains=first,
                last_name__icontains=last,
            ).first()
            if doctor:
                return doctor

        return queryset.filter(
            first_name__icontains=normalized
        ).first() or queryset.filter(last_name__icontains=normalized).first()

    @staticmethod
    def _format_date(date_input):
        if not date_input:
            return None

        date_str = str(date_input).strip().lower()
        today = datetime.now()

        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return date_str

        if date_str == "today":
            return today.strftime("%Y-%m-%d")

        if date_str == "tomorrow":
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")

        weekdays = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        if date_str in weekdays:
            target = weekdays[date_str]
            delta = target - today.weekday()
            if delta <= 0:
                delta += 7
            return (today + timedelta(days=delta)).strftime("%Y-%m-%d")

        return None

    @staticmethod
    def _format_time(time_input):
        if not time_input:
            return None

        time_str = str(time_input).strip().lower()
        
        # Handle HH:MM:SS by stripping seconds if present
        if re.match(r"^\d{1,2}:\d{2}:\d{2}$", time_str):
            time_str = ":".join(time_str.split(":")[:2])

        match = re.match(r"^(\d{1,2})(?::(\d{2}))?(?::(\d{2}))?\s*(am|pm)?$", time_str)
        if not match:
            return None

        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        period = match.group(4) # Group 3 is seconds now if present, but we stripped them above or they are optional here

        if period:
            if period == "pm" and hour != 12:
                hour += 12
            if period == "am" and hour == 12:
                hour = 0

        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return None

        return f"{hour:02d}:{minute:02d}"

    @staticmethod
    def _human_time(time_value):
        try:
            dt = datetime.strptime(time_value, "%H:%M")
            return dt.strftime("%I:%M %p").lstrip("0")
        except Exception:
            return time_value

    @staticmethod
    def _find_available_slot(doctor, date_value, time_value):
        if not doctor or not date_value or not time_value:
            return None

        try:
            return TimeSlot.objects.filter(
                doctor=doctor,
                is_booked=False,
                start_time__date=date_value,
                start_time__time=datetime.strptime(time_value, "%H:%M").time(),
            ).first()
        except Exception:
            return None

    @staticmethod
    def _list_available_slots(doctor, date_value=None):
        query = TimeSlot.objects.filter(doctor=doctor, is_booked=False)
        if date_value:
            query = query.filter(start_time__date=date_value)
        slots = query.order_by("start_time")[:10]
        return [slot.start_time.strftime("%H:%M") for slot in slots]

    @staticmethod
    def _extract_patient_name(user):
        if not user:
            return None
        
        # Try to get full name
        full_name = None
        if hasattr(user, "get_full_name") and callable(user.get_full_name):
            full_name = user.get_full_name()
        
        if not full_name:
            # Fallback to first_name and last_name manually
            first_name = getattr(user, "first_name", "")
            last_name = getattr(user, "last_name", "")
            if first_name or last_name:
                full_name = f"{first_name} {last_name}".strip()
        
        if not full_name:
            # Fallback to username
            full_name = getattr(user, "username", None)
            
        return full_name

    @staticmethod
    def _extract_patient_phone(user):
        if not user:
            return None
        
        # 1. Check direct 'phone' field on user
        phone = getattr(user, "phone", None)
        if phone:
            return phone
            
        # 2. Check 'profile' related object
        try:
            profile = getattr(user, "profile", None)
            if profile:
                return getattr(profile, "phone_number", None) or getattr(profile, "phone", None)
        except Exception:
            pass
            
        # 3. Check 'userprofile' or 'accounts_userprofile_set'
        for attr in ["userprofile", "accounts_userprofile_set"]:
            try:
                related = getattr(user, attr, None)
                if related:
                    # If it's a manager (ForeignKey), get first()
                    if hasattr(related, "first"):
                        related = related.first()
                    if related:
                        return getattr(related, "phone", None) or getattr(related, "phone_number", None)
            except Exception:
                continue
            
        return None

    @staticmethod
    def get_available_tools(category=None):
        return {
            "tools": [
                "chat",
                "book_appointment",
                "get_doctor_slots",
                "cancel_appointment",
                "reschedule_appointment",
                "list_appointments",
                "get_prescriptions",
                "get_notifications",
            ],
            "count": 8,
            "category": category,
        }
