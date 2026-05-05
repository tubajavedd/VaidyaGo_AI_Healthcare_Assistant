"""
Smart Intent Extractor
Extracts appointment details from natural language user messages
"""

import re
from datetime import datetime, timedelta


class SmartIntentExtractor:
    """
    Extracts booking details, parameters, and context from user messages
    """

    @staticmethod
    def extract_appointment_details(message: str) -> dict:
        """
        Extract appointment booking details from natural language
        
        Example inputs:
        - "Book appointment with Dr Smith tomorrow at 10 AM, my name is John, phone 9876543210"
        - "I want to book a slot on Monday, name John Doe, phone +91-9876543210"
        - "Appointment for Alice on 2026-05-10 at 3:30 PM, contact: alice@email.com"
        """
        
        details = {
            "patient_name": None,
            "patient_phone": None,
            "doctor_name": None,
            "doctor_id": None,
            "date": None,
            "time": None,
            "reason": None
        }
        
        lower_msg = message.lower()
        
        # Extract patient name - look for "name is X", "my name X", "I'm X", "this is X"
        name_patterns = [
            r"(?:name\s+(?:is|:)?|i'?m|this\s+is)\s+([a-z\s]+?)(?:,|phone|contact|email|$)",
            r"(?:patient|person)\s+name[:\s]+([a-z\s]+?)(?:,|phone|$)",
        ]
        for pattern in name_patterns:
            match = re.search(pattern, lower_msg, re.IGNORECASE)
            if match:
                details["patient_name"] = match.group(1).strip().title()
                break
        
        # Extract phone number - look for phone/contact patterns
        phone_patterns = [
            r"(?:phone|contact|number|tel)[:\s]+(\+?[0-9\s\-()]{10,})",
            r"([0-9]{3}[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})",
            r"(\+91\s?[0-9]{10})",
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                # Clean up phone number
                phone = re.sub(r'[^\d+]', '', match.group(1))
                details["patient_phone"] = phone
                break
        
        # Extract doctor name - look for "Dr. X", "doctor X"
        doctor_patterns = [
            r"(?:dr\.?|doctor)\s+([a-z\s]+?)(?:,|on|at|$)",
        ]
        for pattern in doctor_patterns:
            match = re.search(pattern, lower_msg, re.IGNORECASE)
            if match:
                details["doctor_name"] = match.group(1).strip().title()
                break
        
        # Extract date - look for specific dates, relative dates
        date_info = SmartIntentExtractor._extract_date(message)
        if date_info:
            details["date"] = date_info["date"]
            details["day_name"] = date_info.get("day_name")
        
        # Extract time - look for time patterns
        time_info = SmartIntentExtractor._extract_time(message)
        if time_info:
            details["time"] = time_info
        
        # Additional cleanup for time extraction if it missed AM/PM logic
        if details["time"] and ("pm" in lower_msg or "am" in lower_msg):
            # If the user said "4pm" but it extracted "04:00", fix it
            if "pm" in lower_msg and int(details["time"].split(':')[0]) < 12:
                h = int(details["time"].split(':')[0]) + 12
                details["time"] = f"{h:02d}:{details['time'].split(':')[1]}"
        
        # Extract reason/purpose
        reason_patterns = [
            r"(?:for|reason|purpose)[:\s]+([a-z\s]+?)(?:,|$)",
            r"(?:consultation|checkup|visit)\s+(?:for|on)\s+([a-z\s]+?)(?:,|$)",
        ]
        for pattern in reason_patterns:
            match = re.search(pattern, lower_msg, re.IGNORECASE)
            if match:
                details["reason"] = match.group(1).strip()
                break
        
        return details

    @staticmethod
    def _extract_date(message: str) -> dict:
        """Extract date information from message"""
        lower_msg = message.lower()
        today = datetime.now()
        
        # Check for relative dates
        if "tomorrow" in lower_msg:
            date = today + timedelta(days=1)
            return {"date": date.strftime("%Y-%m-%d"), "day_name": "tomorrow"}
        
        if "today" in lower_msg:
            return {"date": today.strftime("%Y-%m-%d"), "day_name": "today"}
        
        # Check for day names
        days = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        
        for day_name, day_num in days.items():
            if day_name in lower_msg:
                # Find next occurrence of this day
                current_day = today.weekday()
                days_ahead = day_num - current_day
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                date = today + timedelta(days=days_ahead)
                return {"date": date.strftime("%Y-%m-%d"), "day_name": day_name}
        
        # Check for specific dates (YYYY-MM-DD or DD-MM-YYYY)
        date_patterns = [
            r"(\d{4}-\d{2}-\d{2})",  # 2026-05-10
            r"(\d{1,2})/(\d{1,2})/(\d{4})",  # 10/05/2026 or 5/10/2026
            r"(\d{1,2})-(\d{1,2})-(\d{4})",  # 10-05-2026
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, message)
            if match:
                if len(match.groups()) == 1:
                    # YYYY-MM-DD format
                    return {"date": match.group(1)}
                else:
                    # DD/MM/YYYY or similar
                    day, month, year = match.groups()
                    try:
                        date = datetime(int(year), int(month), int(day))
                        return {"date": date.strftime("%Y-%m-%d")}
                    except ValueError:
                        continue
        
        return None

    @staticmethod
    def _extract_time(message: str) -> str:
        """Extract time from message in HH:MM format"""
        lower_msg = message.lower()
        
        # Improved patterns to handle 4pm, 10am, 4:30 pm etc.
        time_patterns = [
            r"(\d{1,2}):(\d{2})\s*(am|pm)?",
            r"(\d{1,2})\s*(am|pm)",
            r"at\s+(\d{1,2})",
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, lower_msg)
            if match:
                groups = match.groups()
                hour = int(groups[0])
                minute = 0
                
                # Check for minutes in pattern 1
                if ":" in match.group(0):
                    minute = int(groups[1])
                
                # Check for am/pm
                period = None
                for g in groups:
                    if g in ['am', 'pm']:
                        period = g
                
                if period == "pm" and hour != 12:
                    hour += 12
                elif period == "am" and hour == 12:
                    hour = 0
                    
                return f"{hour:02d}:{minute:02d}"
        
        return None

    @staticmethod
    def build_booking_response(message: str, extracted: dict) -> dict:
        """
        Build a conversational response based on extracted details
        """
        if not extracted.get("doctor_name"):
            return {
                "ready_to_book": False,
                "message": "Which doctor would you like to book an appointment with?",
                "missing": ["doctor_name"]
            }

        if not extracted.get("date"):
            return {
                "ready_to_book": False,
                "message": f"For which date would you like to book the appointment with Dr. {extracted['doctor_name']}?",
                "missing": ["date"]
            }

        if not extracted.get("time"):
            return {
                "ready_to_book": False,
                "message": f"What time works for you on {extracted['date']}?",
                "missing": ["time"]
            }

        if not extracted.get("patient_name"):
            return {
                "ready_to_book": False,
                "message": "May I know the patient's name for this booking?",
                "missing": ["patient_name"]
            }

        return {
            "ready_to_book": True,
            "extracted": extracted,
            "message": f"Great! I have all the details to book your appointment with Dr. {extracted['doctor_name']} on {extracted['date']} at {extracted['time']}."
        }
