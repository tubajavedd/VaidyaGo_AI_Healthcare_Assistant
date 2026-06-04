import logging
from datetime import datetime, timedelta
from django.db import transaction
from DoctorSlot.models import TimeSlot, DoctorSlot
from Dr_personalInfo.models import DoctorPersonalInfo
from appointments.models import Appointment

logger = logging.getLogger(__name__)

class ToolRouter:
    @staticmethod
    def handle(action, data, user):
        """
        Routes the action to the appropriate handler.
        """
        if not user or user.role not in ["DOCTOR", "ADMIN"]:
            return {
                "message": "This action requires a doctor or admin account.",
                "action_executed": False,
                "data": {},
            }

        doctor = ToolRouter._get_doctor_profile(user, data)
        if not doctor:
            email = user.email or "N/A"
            phone = getattr(user, 'phone', "N/A")
            return {
                "message": f"I could not find your doctor profile linked to this account (Email: {email}, Phone: {phone}). Please ensure you have completed all 4 onboarding forms with these details.",
                "action_executed": False,
                "data": {},
            }

        handlers = {
            "get_my_slots": ToolRouter._get_my_slots,
            "generate_slots": ToolRouter._generate_slots,
            "delete_slot": ToolRouter._delete_slot,
            "delete_all_slots": ToolRouter._delete_all_slots,
            "get_my_appointments": ToolRouter._get_my_appointments,
            "get_doctor_profile": ToolRouter._get_doctor_profile_handler,
            "get_professional_info": ToolRouter._get_professional_info,
            "get_hospital_info": ToolRouter._get_hospital_info,
            "list_doctor_documents": ToolRouter._list_doctor_documents,
            "accept_appointment": ToolRouter._accept_appointment,
            "reject_appointment": ToolRouter._reject_appointment,
            "cancel_appointment": ToolRouter._cancel_appointment,
            "get_notifications": ToolRouter._get_notifications,
            "update_doctor_profile": ToolRouter._update_doctor_profile,
            "update_professional_info": ToolRouter._update_professional_info,
            "update_hospital_info": ToolRouter._update_hospital_info,
            "remind_appointments": ToolRouter._remind_appointments,
            "get_pending_appointments": ToolRouter._get_pending_appointments,
            "get_recent_patients": ToolRouter._get_recent_patients,
            "submit_for_approval": ToolRouter._submit_for_approval,
            "reschedule_appointment": ToolRouter._reschedule_appointment,
            "get_appointment_details": ToolRouter._get_appointment_details,
            "create_appointment": ToolRouter._create_appointment,
        }

        handler = handlers.get(action)
        if handler:
            return handler(data, doctor)
        
        return {
            "message": f"Action '{action}' is not supported yet.",
            "action_executed": False,
            "data": {},
        }

    @staticmethod
    def _get_doctor_profile(user, data=None):
        from django.db.models import Q
        from AdminLogin.models import Profile
        
        # 1. Check if doctor_id is provided in the data (highest priority)
        if data and data.get("doctor_id"):
            try:
                return DoctorPersonalInfo.objects.get(id=data.get("doctor_id"))
            except DoctorPersonalInfo.DoesNotExist:
                logger.warning(f"doctor_id {data.get('doctor_id')} provided but not found.")

        if not user or user.is_anonymous:
            return None

        try:
            email = (user.email or "").strip()
            username = (user.username or "").strip()
            phone = getattr(user, 'phone', "")
            if phone: phone = phone.strip()
            
            logger.info(f"Looking up doctor profile for User(id={user.id}, email={email}, username={username}, phone={phone})")
            
            # Start with email match (case-insensitive)
            # Try matching user email or username against doctor email
            query = Q(email__iexact=email) if email else Q(id=-1)
            if username and "@" in username: # If username is an email
                query |= Q(email__iexact=username)
            
            # Add phone matching (very aggressive)
            if phone:
                clean_phone = ''.join(filter(str.isdigit, phone))
                query |= Q(mobile_number__contains=phone)
                if len(clean_phone) >= 10:
                    query |= Q(mobile_number__contains=clean_phone[-10:])
                
                if phone.startswith('+91'):
                    query |= Q(mobile_number=phone[3:])
                elif not phone.startswith('+'):
                    query |= Q(mobile_number='+91' + phone)

            # Try to check linked Profile phone number
            try:
                profile = Profile.objects.filter(user=user).first()
                if profile and profile.phone_number:
                    p_phone = profile.phone_number.strip()
                    query |= Q(mobile_number__contains=p_phone)
                    clean_p_phone = ''.join(filter(str.isdigit, p_phone))
                    if len(clean_p_phone) >= 10:
                        query |= Q(mobile_number__contains=clean_p_phone[-10:])
            except Exception as pe:
                logger.debug(f"Profile lookup failed: {str(pe)}")
            
            doctor = DoctorPersonalInfo.objects.filter(query).first()
            
            # Fallback: Search by name if username looks like a name
            if not doctor and username and len(username) > 3:
                doctor = DoctorPersonalInfo.objects.filter(
                    Q(first_name__iexact=username) | 
                    Q(last_name__iexact=username)
                ).first()

            if doctor:
                logger.info(f"Successfully matched doctor: {doctor.id} ({doctor.first_name})")
            else:
                logger.warning(f"Failed to find DoctorPersonalInfo for User {user.id}")
                
            return doctor
        except Exception as e:
            logger.error(f"Error in _get_doctor_profile: {str(e)}")
            return None

    @staticmethod
    def _get_my_slots(data, doctor):
        from django.utils import timezone
        import datetime
        
        date_str = data.get("date")
        target_date = timezone.now().date()
        
        if date_str:
            if date_str.lower() == "today":
                target_date = timezone.now().date()
            elif date_str.lower() == "tomorrow":
                target_date = timezone.now().date() + datetime.timedelta(days=1)
            else:
                try:
                    target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass
        
        logger.info(f"Fetching slots for doctor {doctor.id} on date {target_date}")
        
        slots = TimeSlot.objects.filter(
            doctor=doctor, 
            start_time__date=target_date
        ).order_by("start_time")

        if not slots.exists():
            return {
                "message": f"I couldn't find any available slots for {target_date.strftime('%A, %b %d')}. Would you like me to generate your standard morning and evening slots for you?",
                "action_executed": True,
                "data": {"slots": [], "suggestion": "generate_slots"},
            }

        slot_list = [
            {
                "id": s.id,
                "start": s.start_time.strftime("%I:%M %p"),
                "end": s.end_time.strftime("%I:%M %p"),
                "date": s.start_time.strftime("%Y-%m-%d"),
                "booked": s.is_booked
            }
            for s in slots
        ]

        return {
            "message": f"I found {len(slot_list)} slots for you on {target_date.strftime('%A, %b %d')}.",
            "action_executed": True,
            "data": {"slots": slot_list},
        }

    @staticmethod
    def _generate_slots(data, doctor):
        from DoctorSlot.models import DoctorSlot, TimeSlot
        from DoctorSlot.utils import generate_timeslots_from_template
        from django.utils import timezone
        import datetime

        # 1. Parse Dates (Support relative 'today', 'tomorrow')
        today = timezone.now().date()
        
        def parse_date(d_str, default):
            if not d_str: return default
            d_str = str(d_str).lower().strip()
            if d_str == "today": return today
            if d_str == "tomorrow": return today + datetime.timedelta(days=1)
            try:
                return datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
            except ValueError:
                return default

        # 2. Robust Time Parsing (Handles 10am, 2pm, 10:00 AM, etc.)
        def parse_time(t_str, default):
            if not t_str: return default
            t_str = str(t_str).lower().strip().replace(" ", "")
            formats = ["%H:%M", "%I%p", "%I:%M%p", "%H:%M:%S"]
            for fmt in formats:
                try:
                    return datetime.datetime.strptime(t_str, fmt).time()
                except ValueError:
                    continue
            return default

        try:
            start_date = parse_date(data.get("start_date") or data.get("date"), today)
            end_date = parse_date(data.get("end_date"), start_date)
            from_time = parse_time(data.get("from_time"), datetime.time(10, 0))
            to_time = parse_time(data.get("to_time"), datetime.time(13, 0))
            
            # 3. Robust Duration Parsing (Extract digits from "10min" or "30 mins")
            duration_val = data.get("slot_duration") or 30
            if isinstance(duration_val, str):
                import re
                match = re.search(r'\d+', duration_val)
                duration = int(match.group()) if match else 30
            else:
                duration = int(duration_val)

            # Create a DoctorSlot template record
            doctor_slot = DoctorSlot.objects.create(
                doctor=doctor,
                from_date=start_date,
                to_date=end_date,
                from_time=from_time,
                to_time=to_time,
                slot_duration=duration,
                is_active=True
            )
            
            # Generate the individual TimeSlot records
            generate_timeslots_from_template(doctor_slot)
            
            # Count how many slots were created/exist for the start date
            new_slots_count = TimeSlot.objects.filter(
                doctor=doctor, 
                start_time__date__range=(start_date, end_date)
            ).count()

            date_range_str = f"on {start_date.strftime('%b %d, %Y')}" if start_date == end_date else f"from {start_date.strftime('%b %d')} to {end_date.strftime('%b %d, %Y')}"
            time_range_str = f"between {from_time.strftime('%I:%M %p')} and {to_time.strftime('%I:%M %p')}"
            
            return {
                "message": f"I have successfully generated your availability {date_range_str} {time_range_str} with {duration}-minute slots. You now have {new_slots_count} total slots in this period.",
                "action_executed": True,
                "data": {
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "slots_count": new_slots_count
                },
            }
        except Exception as e:
            logger.error(f"Error in _generate_slots: {str(e)}")
            return {
                "message": f"I encountered an error while generating your slots: {str(e)}",
                "action_executed": False,
                "data": {},
            }

    @staticmethod
    def _parse_time_string(time_str):
        import datetime
        if not time_str:
            return None
        time_str = str(time_str).strip().lower().replace(" ", "")
        formats = ["%H:%M", "%I%p", "%I:%M%p", "%H%M"]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(time_str, fmt).time()
            except ValueError:
                continue
        return None

    @staticmethod
    def _delete_slot(data, doctor):
        slot_id = data.get("slot_id")
        date_str = data.get("date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if slot_id:
            slot = TimeSlot.objects.filter(id=slot_id, doctor=doctor).first()
            if not slot:
                return {
                    "message": f"I could not find a slot with id {slot_id} for your profile.",
                    "action_executed": False,
                    "data": {}
                }
            slot.delete()
            return {
                "message": f"Slot {slot_id} has been deleted successfully.",
                "action_executed": True,
                "data": {"deleted_slot_id": slot_id}
            }

        if date_str and start_time:
            parsed_time = ToolRouter._parse_time_string(start_time)
            if not parsed_time:
                return {
                    "message": "I could not parse the start time you provided. Use HH:MM or 10:00 AM format.",
                    "action_executed": False,
                    "data": {}
                }
            slots = TimeSlot.objects.filter(
                doctor=doctor,
                start_time__date=date_str,
                start_time__time=parsed_time
            )
            if not slots.exists():
                return {
                    "message": f"No slot found on {date_str} at {start_time}.",
                    "action_executed": False,
                    "data": {}
                }
            deleted_count = slots.count()
            slots.delete()
            return {
                "message": f"Deleted {deleted_count} slot(s) on {date_str} at {start_time}.",
                "action_executed": True,
                "data": {"deleted_count": deleted_count}
            }

        if date_str:
            slots = TimeSlot.objects.filter(doctor=doctor, start_time__date=date_str)
            if not slots.exists():
                return {
                    "message": f"No slots found on {date_str} to delete.",
                    "action_executed": False,
                    "data": {}
                }
            deleted_count = slots.count()
            slots.delete()
            return {
                "message": f"Deleted {deleted_count} slot(s) for {date_str}.",
                "action_executed": True,
                "data": {"deleted_count": deleted_count}
            }

        return {
            "message": "Please tell me the slot to delete by slot_id, or provide a date and time, or say delete all slots.",
            "action_executed": False,
            "data": {}
        }

    @staticmethod
    def _delete_all_slots(data, doctor):
        delete_all = data.get("all") or data.get("delete_all") or data.get("confirm")
        date_str = data.get("date")

        if date_str:
            slots = TimeSlot.objects.filter(doctor=doctor, start_time__date=date_str)
            if not slots.exists():
                return {
                    "message": f"No slots found on {date_str} to delete.",
                    "action_executed": False,
                    "data": {}
                }
            deleted_count = slots.count()
            slots.delete()
            return {
                "message": f"Deleted {deleted_count} slot(s) on {date_str}.",
                "action_executed": True,
                "data": {"deleted_count": deleted_count}
            }

        if delete_all in [True, "true", "yes", "all", "delete_all", "confirm"] or data.get("delete") == "all":
            slots = TimeSlot.objects.filter(doctor=doctor)
            deleted_count = slots.count()
            slots.delete()
            return {
                "message": f"Deleted all {deleted_count} slots for your profile.",
                "action_executed": True,
                "data": {"deleted_count": deleted_count}
            }

        return {
            "message": "Please confirm you want to delete all slots by saying 'delete all slots' or provide a date to delete slots for that date.",
            "action_executed": False,
            "data": {}
        }

    @staticmethod
    def _get_my_appointments(data, doctor):
        date_str = data.get("date")
        query = Appointment.objects.filter(doctor=doctor)
        
        if date_str:
            query = query.filter(start_time__date=date_str)
        
        appointments = query.order_by("start_time")
        if not appointments.exists():
            return {
                "message": "You have no appointments scheduled.",
                "action_executed": True,
                "data": {"appointments": []},
            }

        appt_list = [
            {
                "id": a.id,
                "patient": a.patient_name,
                "time": a.start_time.strftime("%I:%M %p"),
                "date": a.start_time.strftime("%Y-%m-%d"),
                "status": a.status
            }
            for a in appointments
        ]

        return {
            "message": f"You have {len(appt_list)} appointments scheduled for {date_str if date_str else 'today'}.",
            "action_executed": True,
            "data": {"appointments": appt_list},
        }

    @staticmethod
    def _get_doctor_profile_handler(data, doctor):
        return {
            "message": f"Here is your profile info: Dr. {doctor.first_name} {doctor.last_name}, specializing in {doctor.city}.",
            "action_executed": True,
            "data": {
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "email": doctor.email,
                "city": doctor.city,
                "status": doctor.status
            },
        }

    @staticmethod
    def _get_professional_info(data, doctor):
        try:
            from Dr_professionalInfo.models import DoctorProfessionalInfo
            info = DoctorProfessionalInfo.objects.get(doctor=doctor)
            return {
                "message": f"Your professional info: Department: {info.department}, Specialization: {info.specialization}, Experience: {info.years_of_experience} years.",
                "action_executed": True,
                "data": {
                    "department": info.department,
                    "specialization": info.specialization,
                    "experience": info.years_of_experience,
                    "license": info.medical_license_number
                }
            }
        except Exception:
            return {"message": "Professional info not found.", "action_executed": False, "data": {}}

    @staticmethod
    def _get_hospital_info(data, doctor):
        try:
            from Dr_hospitalInfo.models import DoctorHospitalInfo
            info = DoctorHospitalInfo.objects.get(doctor=doctor)
            return {
                "message": f"Hospital info: Type: {info.employment_type}, Fees: {info.consultation_fees}, Leave day: {info.leave_day}.",
                "action_executed": True,
                "data": {
                    "employment_type": info.employment_type,
                    "fees": str(info.consultation_fees),
                    "leave_day": info.leave_day
                }
            }
        except Exception:
            return {"message": "Hospital info not found.", "action_executed": False, "data": {}}

    @staticmethod
    def _list_doctor_documents(data, doctor):
        try:
            from Dr_Documents.models import DoctorDocument
            docs = DoctorDocument.objects.filter(doctor=doctor)
            if not docs.exists():
                return {"message": "No documents uploaded yet.", "action_executed": True, "data": {"documents": []}}
            
            doc_list = [{"type": d.document_type, "status": d.status} for d in docs]
            return {
                "message": f"You have {len(doc_list)} documents uploaded.",
                "action_executed": True,
                "data": {"documents": doc_list}
            }
        except Exception:
            return {"message": "Error fetching documents.", "action_executed": False, "data": {}}

    @staticmethod
    def _accept_appointment(data, doctor):
        appointment_id = data.get("appointment_id")
        if not appointment_id:
            return {"message": "I need an appointment ID to accept it.", "action_executed": False, "data": {}}
        
        try:
            from appointments.views import accept_appointment
            # We mock the request object for the view
            class MockRequest:
                def __init__(self, data): self.data = data
            
            response = accept_appointment(MockRequest(data), appointment_id)
            if response.status_code == 200:
                return {"message": response.data["message"], "action_executed": True, "data": response.data.get("data", {})}
            return {"message": response.data.get("error", "Failed to accept appointment."), "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error accepting appointment: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _reject_appointment(data, doctor):
        appointment_id = data.get("appointment_id")
        if not appointment_id:
            return {"message": "I need an appointment ID to reject it.", "action_executed": False, "data": {}}
        
        try:
            from appointments.views import reject_appointment
            class MockRequest:
                def __init__(self, data): self.data = data
            
            response = reject_appointment(MockRequest(data), appointment_id)
            if response.status_code == 200:
                return {"message": response.data["message"], "action_executed": True, "data": {}}
            return {"message": response.data.get("error", "Failed to reject appointment."), "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error rejecting appointment: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _cancel_appointment(data, doctor):
        appointment_id = data.get("appointment_id")
        if not appointment_id:
            return {"message": "I need an appointment ID to cancel it.", "action_executed": False, "data": {}}
        
        try:
            from appointments.views import cancel_appointment
            class MockRequest:
                def __init__(self, data): self.data = data
            
            response = cancel_appointment(MockRequest(data), appointment_id)
            if response.status_code == 200:
                return {"message": response.data["message"], "action_executed": True, "data": {}}
            return {"message": response.data.get("error", "Failed to cancel appointment."), "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error cancelling appointment: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _get_notifications(data, doctor):
        try:
            from Notifications.models import Notification
            # Notifications are linked to User, not DoctorPersonalInfo
            # We need to find the user by email
            from AdminLogin.models import User
            user = User.objects.get(email=doctor.email)
            
            query = Notification.objects.filter(user=user)
            if data.get("unread_only"):
                query = query.filter(is_read=False)
            
            notifs = query.order_by("-created_at")[:10]
            if not notifs.exists():
                return {"message": "You have no notifications.", "action_executed": True, "data": {"notifications": []}}
            
            notif_list = [{"id": n.id, "title": n.title, "message": n.message, "read": n.is_read} for n in notifs]
            msg = f"You have {len(notif_list)} notifications:\n" + "\n".join([f"- {n['title']}: {n['message']}" for n in notif_list])
            
            return {
                "message": msg,
                "action_executed": True,
                "data": {"notifications": notif_list}
            }
        except Exception as e:
            return {"message": f"Error fetching notifications: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _update_doctor_profile(data, doctor):
        try:
            for key, value in data.items():
                if hasattr(doctor, key) and key not in ['id', 'email']:
                    setattr(doctor, key, value)
            doctor.save()
            return {"message": "Your profile has been updated successfully.", "action_executed": True, "data": {}}
        except Exception as e:
            return {"message": f"Error updating profile: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _update_professional_info(data, doctor):
        try:
            from Dr_professionalInfo.models import DoctorProfessionalInfo
            info, created = DoctorProfessionalInfo.objects.get_or_create(doctor=doctor)
            for key, value in data.items():
                if hasattr(info, key):
                    setattr(info, key, value)
            info.save()
            return {"message": "Professional information updated.", "action_executed": True, "data": {}}
        except Exception as e:
            return {"message": f"Error updating professional info: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _update_hospital_info(data, doctor):
        try:
            from Dr_hospitalInfo.models import DoctorHospitalInfo
            info, created = DoctorHospitalInfo.objects.get_or_create(doctor=doctor)
            for key, value in data.items():
                if hasattr(info, key):
                    setattr(info, key, value)
            info.save()
            return {"message": "Hospital/Employment information updated.", "action_executed": True, "data": {}}
        except Exception as e:
            return {"message": f"Error updating hospital info: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _remind_appointments(data, doctor):
        try:
            from appointments.models import Appointment
            from django.utils import timezone
            from django.core.mail import send_mail
            from django.conf import settings
            from Notifications.models import Notification
            from AdminLogin.models import User
            
            today = timezone.now().date()
            appointments = Appointment.objects.filter(doctor=doctor, start_time__date=today, status='confirmed')
            
            if not appointments.exists():
                return {"message": "You have no confirmed appointments for today.", "action_executed": True, "data": {}}
            
            # Format message
            appt_list = [f"- {a.patient_name} at {a.start_time.strftime('%H:%M')}" for a in appointments]
            msg_content = f"Reminder: You have {len(appointments)} appointments today:\n" + "\n".join(appt_list)
            
            # 1. Email Notification
            send_mail(
                subject="Today's Appointment Reminder - VaidyaGo",
                message=msg_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor.email],
                fail_silently=True
            )
            
            # 2. App Notification
            try:
                user = User.objects.get(email=doctor.email)
                Notification.objects.create(user=user, title="Daily Schedule Reminder", message=msg_content)
            except:
                pass
                
            return {
                "message": f"I've sent a reminder of your {len(appointments)} appointments today to your email and notifications.",
                "action_executed": True,
                "data": {"count": len(appointments)}
            }
        except Exception as e:
            return {"message": f"Error sending reminder: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _reschedule_appointment(data, doctor):
        appointment_id = data.get("appointment_id")
        slot_id = data.get("slot_id")
        reason = data.get("reason")
        
        if not appointment_id or not slot_id:
            return {"message": "I need both an appointment ID and a new slot ID to reschedule.", "action_executed": False, "data": {}}
        
        try:
            from appointments.views import reschedule_appointment
            class MockRequest:
                def __init__(self, data): self.data = data
            
            response = reschedule_appointment(MockRequest(data), appointment_id)
            if response.status_code == 200:
                return {"message": response.data["message"], "action_executed": True, "data": response.data.get("data", {})}
            return {"message": response.data.get("error", "Failed to reschedule appointment."), "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error rescheduling appointment: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _get_appointment_details(data, doctor):
        appointment_id = data.get("appointment_id")
        if not appointment_id:
            return {"message": "Please provide an appointment ID.", "action_executed": False, "data": {}}
        
        try:
            from appointments.models import Appointment
            appt = Appointment.objects.get(id=appointment_id, doctor=doctor)
            
            details = {
                "id": appt.id,
                "patient": appt.patient_name,
                "phone": appt.patient_phone,
                "email": appt.patient_email,
                "time": appt.start_time.strftime("%H:%M"),
                "date": appt.start_time.strftime("%Y-%m-%d"),
                "status": appt.status,
                "type": appt.appointment_type,
                "location": appt.location,
                "reason": appt.rejection_reason or appt.reschedule_reason
            }
            
            msg = f"Details for appointment #{appt.id}:\n"
            msg += f"- Patient: {appt.patient_name}\n"
            msg += f"- Time: {appt.start_time.strftime('%Y-%m-%d %H:%M')}\n"
            msg += f"- Status: {appt.status}\n"
            if appt.location: msg += f"- Location: {appt.location}\n"
            if appt.appointment_type: msg += f"- Type: {appt.appointment_type}\n"
            
            return {
                "message": msg,
                "action_executed": True,
                "data": details
            }
        except Appointment.DoesNotExist:
            return {"message": "Appointment not found or not assigned to you.", "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error fetching details: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _create_appointment(data, doctor):
        slot_id = data.get("slot_id") or data.get("slot")
        patient_name = data.get("patient_name")
        patient_phone = data.get("patient_phone")
        patient_email = data.get("patient_email")
        
        if not slot_id or not patient_name or not patient_phone:
            return {
                "message": "To book an appointment, I need the Slot ID, Patient Name, and Patient Phone number.",
                "action_executed": False,
                "data": {}
            }
        
        # Format data for the view
        request_data = {
            "slot": slot_id,
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "patient_email": patient_email,
            "appointment_type": data.get("appointment_type", "General Checkup"),
            "location": data.get("location", "Clinic")
        }

        try:
            from appointments.views import create_appointment
            class MockRequest:
                def __init__(self, data): self.data = data
            
            response = create_appointment(MockRequest(request_data))
            if response.status_code == 201:
                return {
                    "message": f"Appointment successfully booked for {patient_name} at {response.data.get('start_time')}.",
                    "action_executed": True,
                    "data": response.data
                }
            return {"message": response.data.get("error", "Failed to create appointment."), "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error creating appointment: {str(e)}", "action_executed": False, "data": {}}
    @staticmethod
    def _get_pending_appointments(data, doctor):
        try:
            pending = Appointment.objects.filter(doctor=doctor, status='pending').order_by("-start_time")
            if not pending.exists():
                return {"message": "You have no pending appointment requests.", "action_executed": True, "data": {"appointments": []}}
            
            appt_list = [
                {
                    "id": a.id,
                    "patient": a.patient_name,
                    "time": a.start_time.strftime("%H:%M"),
                    "date": a.start_time.strftime("%Y-%m-%d"),
                    "type": a.appointment_type
                }
                for a in pending
            ]
            msg = f"You have {len(appt_list)} pending requests:\n" + "\n".join([f"- {a['patient']} ({a['date']} at {a['time']})" for a in appt_list])
            return {"message": msg, "action_executed": True, "data": {"appointments": appt_list}}
        except Exception as e:
            return {"message": f"Error fetching pending appointments: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _get_recent_patients(data, doctor):
        try:
            recent = Appointment.objects.filter(doctor=doctor, status='outpatient').order_by("-start_time")[:10]
            if not recent.exists():
                return {"message": "You have no recent patient records.", "action_executed": True, "data": {"patients": []}}
            
            patient_list = [
                {
                    "id": a.id,
                    "patient": a.patient_name,
                    "date": a.start_time.strftime("%Y-%m-%d"),
                    "disease": a.patient_disease or "N/A"
                }
                for a in recent
            ]
            msg = f"Your recently consulted patients:\n" + "\n".join([f"- {p['patient']} (Visited: {p['date']})" for p in patient_list])
            return {"message": msg, "action_executed": True, "data": {"patients": patient_list}}
        except Exception as e:
            return {"message": f"Error fetching recent patients: {str(e)}", "action_executed": False, "data": {}}

    @staticmethod
    def _submit_for_approval(data, doctor):
        try:
            from Dr_personalInfo.views import DoctorSubmitView
            # Create a mock request
            class MockRequest:
                def __init__(self, user): self.user = user
            
            view = DoctorSubmitView()
            response = view.post(MockRequest(None), pk=doctor.id) # pk is doctor_id
            
            if response.status_code == 200:
                return {"message": "Your profile has been submitted for administrator approval. You will be notified once reviewed.", "action_executed": True, "data": {}}
            return {"message": "Submission failed. Please ensure all profile sections are complete.", "action_executed": False, "data": {}}
        except Exception as e:
            return {"message": f"Error during submission: {str(e)}", "action_executed": False, "data": {}}
