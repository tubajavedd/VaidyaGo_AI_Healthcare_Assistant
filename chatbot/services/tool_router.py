import requests
import logging
import re
import json
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User

from chatbot.services.tools_registry import ToolsRegistry

logger = logging.getLogger(__name__)


class ToolRouter:
    """
    Routes and executes available tools/APIs based on user intent
    """

    @staticmethod
    def execute(intent_data, user):
        """
        Execute the appropriate tool based on intent
        """

        action = intent_data.get("action")
        data = intent_data.get("data", {})
        message = intent_data.get("message", "")

        # If no action, just return the message
        if not action:
            return {
                "message": message,
                "action_executed": False
            }

        # Check if tool exists in registry
        tool = ToolsRegistry.get_tool(action)
        if not tool:
            return {
                "message": f"I don't have access to the '{action}' action.",
                "action_executed": False
            }

        # Auto-fill missing information based on action
        data = ToolRouter._auto_fill_missing_info(action, data, user)

        # Check for required parameters after auto-fill
        missing_params = ToolRouter._validate_parameters(tool, data)
        if missing_params:
            return {
                "message": f"{message}\n\nMissing required information: {', '.join(missing_params)}",
                "action_executed": False,
                "missing_parameters": missing_params
            }

        try:
            # Execute the tool
            result = ToolRouter._execute_tool(action, tool, data, user)
            result["action_executed"] = True
            return result
        except Exception as e:
            logger.error(f"Error executing tool {action}: {str(e)}")
            return {
                "message": f"Error executing {action}: {str(e)}",
                "action_executed": False,
                "error": str(e)
            }

    @staticmethod
    def _auto_fill_missing_info(action, data, user):
        """
        Auto-fill missing information for specific actions.
        Currently handles:
        - book_appointment: Fill patient_name, patient_phone from user profile
                          Fill slot ID by resolving doctor + date + time
        """
        if action == "book_appointment":
            # 1. Auto-fill patient info from authenticated user
            data = ToolRouter._auto_fill_patient_info(data, user)
            
            # 2. Auto-resolve slot ID if missing
            data = ToolRouter._auto_resolve_slot(data)
        
        return data

    @staticmethod
    def _auto_fill_patient_info(data, user):
        """
        Auto-fill patient_name and patient_phone from authenticated user's profile
        """
        # Check if patient_name or patient_phone are missing
        needs_name = "patient_name" not in data or not data.get("patient_name")
        needs_phone = "patient_phone" not in data or not data.get("patient_phone")
        
        if not needs_name and not needs_phone:
            return data  # Nothing to fill
        
        # Try to get info from authenticated user
        if user and user.is_authenticated:
            try:
                # Try to get user profile from user profile API
                base_url = "http://localhost:8000"
                profile_url = f"{base_url}/auth/profile/"
                headers = {"Content-Type": "application/json"}
                
                response = requests.get(profile_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    profile_data = response.json()
                    user_profile = profile_data.get("user", {})
                    
                    if needs_name and not data.get("patient_name"):
                        # Try to get name from profile
                        profile_name = user_profile.get("name") or user_profile.get("first_name")
                        if profile_name:
                            data["patient_name"] = profile_name
                        elif user.get_full_name():
                            data["patient_name"] = user.get_full_name()
                        elif user.username:
                            data["patient_name"] = user.username
                    
                    if needs_phone and not data.get("patient_phone"):
                        phone = user_profile.get("phone") or user_profile.get("phone_number")
                        if phone:
                            data["patient_phone"] = phone
                            
            except Exception as e:
                logger.warning(f"Failed to auto-fill patient info from profile: {str(e)}")
        
        return data

    @staticmethod
    def _auto_resolve_slot(data):
        """
        Auto-resolve slot ID from doctor name, date, and time.
        If slot is missing but doctor_name, date, and time are provided,
        fetch available slots and find the matching one.
        """
        if "slot" in data and data.get("slot"):
            return data  # Slot already provided
        
        # Check if we have enough info to resolve slot
        doctor_id = data.get("doctor_id")
        doctor_name = data.get("doctor_name")
        date = data.get("date")
        time = data.get("time")
        
        if not (date and time and (doctor_id or doctor_name)):
            logger.debug("Insufficient info to auto-resolve slot")
            return data
        
        # First, resolve doctor_name to doctor_id if needed
        if not doctor_id and doctor_name:
            doctor_id = ToolRouter._resolve_doctor_id(doctor_name)
            if not doctor_id:
                logger.warning(f"Could not resolve doctor ID for: {doctor_name}")
                return data
            data["doctor_id"] = doctor_id
        
        # Try to get slot ID
        try:
            base_url = "http://localhost:8000"
            # Format the date if needed (convert day name to date)
            formatted_date = ToolRouter._format_date(date)
            
            slots_url = f"{base_url}/api/doctor/{doctor_id}/slots/?date={formatted_date}"
            headers = {"Content-Type": "application/json"}
            
            response = requests.get(slots_url, headers=headers, timeout=10)
            if response.status_code == 200:
                slots_data = response.json()
                available_slots = slots_data.get("available_slots", [])
                
                # Try to find matching slot by time
                for slot in available_slots:
                    slot_time = slot.get("time")
                    slot_id = slot.get("id")
                    
                    if slot_time == time:
                        data["slot"] = slot_id
                        logger.info(f"Auto-resolved slot ID: {slot_id} for time {time}")
                        return data
                
                # If exact match not found, try partial match
                # E.g., "10:00" might match "10:00:00"
                for slot in available_slots:
                    slot_time = slot.get("time", "")
                    slot_id = slot.get("id")
                    
                    # Remove seconds for comparison
                    if slot_time and time:
                        slot_time_clean = slot_time.split(":")[0] + ":" + slot_time.split(":")[1] if ":" in slot_time else slot_time
                        time_clean = time.split(":")[0] + ":" + time.split(":")[1] if ":" in time else time
                        
                        if slot_time_clean == time_clean:
                            data["slot"] = slot_id
                            logger.info(f"Auto-resolved slot ID: {slot_id} for time {time}")
                            return data
                            
        except Exception as e:
            logger.warning(f"Failed to auto-resolve slot: {str(e)}")
        
        return data

    @staticmethod
    def _resolve_doctor_id(doctor_name):
        """
        Resolve doctor_name to doctor_id by searching doctors
        """
        try:
            base_url = "http://localhost:8000"
            # Try to search for doctor by name
            search_url = f"{base_url}/api/doctors/search/?name={doctor_name}"
            headers = {"Content-Type": "application/json"}
            
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code == 200:
                doctors = response.json()
                if doctors:
                    return doctors[0].get("id")
            
            # Alternative: try to list doctors and find by name
            list_url = f"{base_url}/api/doctors/list/"
            response = requests.get(list_url, headers=headers, timeout=10)
            if response.status_code == 200:
                doctors = response.json()
                for doctor in doctors:
                    doc_name = doctor.get("name", "") or doctor.get("first_name", "") or ""
                    if doctor_name.lower() in doc_name.lower():
                        return doctor.get("id")
                        
        except Exception as e:
            logger.warning(f"Failed to resolve doctor ID: {str(e)}")
        
        return None

    @staticmethod
    def _format_date(date_input):
        """
        Format date input to YYYY-MM-DD format.
        Handles day names like 'monday', 'tuesday', etc.
        """
        from datetime import datetime, timedelta
        
        date_str = str(date_input).strip().lower()
        
        # If already in YYYY-MM-DD format, return as-is
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            return date_str
        
        # Map day names to day offsets
        today = datetime.now()
        day_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }
        
        if date_str in day_map:
            # Calculate days until the target day
            current_day = today.weekday()
            target_day = day_map[date_str]
            days_ahead = target_day - current_day
            if days_ahead <= 0:  # Target day is today or already passed this week
                days_ahead += 7  # Next week's occurrence
            
            target_date = today + timedelta(days=days_ahead)
            return target_date.strftime("%Y-%m-%d")
        
        # Try parsing as other date formats
        try:
            parsed = datetime.strptime(date_str, "%d-%m-%Y")
            return parsed.strftime("%Y-%m-%d")
        except:
            pass
        
        # Return original if can't parse
        return date_input

    @staticmethod
    def _validate_parameters(tool, data):
        """
        Check if all required parameters are present
        Returns list of missing parameters, empty if all present
        """
        missing = []
        params = tool.get("parameters", {})
        
        for param_name, param_info in params.items():
            is_required = param_info.get("required", True)
            if not is_required:
                continue

            # Parameters in URL are still required but handled separately
            if "{" + param_name + "}" in tool.get("endpoint", ""):
                if param_name not in data or data[param_name] is None or data[param_name] == "":
                    missing.append(param_name)
                continue

            if param_name not in data or data[param_name] is None or data[param_name] == "":
                missing.append(param_name)

        return missing


    @staticmethod
    def _execute_tool(action_name, tool, data, user):
        """
        Execute a specific tool/API
        """

        # Get base URL - adjust this to your actual domain
        base_url = "http://localhost:8000"  # Change to your production URL
        endpoint = tool.get("endpoint", "")
        method = tool.get("method", "GET").upper()

        # Build full URL with path parameters
        url = ToolRouter._build_url(base_url, endpoint, data)

        # Prepare headers
        headers = {
            "Content-Type": "application/json"
        }

        # Add authentication token if user is authenticated
        if user and user.is_authenticated:
            # If you're using token authentication, add it here
            headers["Authorization"] = f"Bearer {user.auth_token}"
            pass

        logger.debug(f"Executing tool: {action_name}, URL: {url}, Method: {method}")

        # Execute based on HTTP method
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=30)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return {
                "message": f"Unsupported HTTP method: {method}",
                "error": "invalid_method"
            }

        # Handle response
        if response.status_code in [200, 201, 202]:
            try:
                result = response.json()
                return {
                    "message": result.get("message", f"{action_name} executed successfully"),
                    "data": result,
                    "status": "success"
                }
            except Exception as e:
                return {
                    "message": f"{action_name} executed successfully",
                    "status": "success",
                    "data": response.text
                }
        else:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text

            logger.error(f"Tool {action_name} returned status {response.status_code}: {error_detail}")
            return {
                "message": f"Error executing {action_name}: {error_detail}",
                "error": error_detail,
                "status": "error"
            }

    @staticmethod
    def _build_url(base_url, endpoint, data):
        """
        Build URL by replacing path parameters
        
        Example: 
        - endpoint: "/api/appointments/{appointment_id}/cancel/"
        - data: {"appointment_id": 123, "reason": "..."}
        - result: "/api/appointments/123/cancel/"
        """
        url = endpoint
        
        # Find all path parameters in format {param_name}
        param_pattern = r'\{(\w+)\}'
        params_found = re.findall(param_pattern, url)
        
        # Replace each parameter with value from data
        for param in params_found:
            if param in data:
                url = url.replace(f"{{{param}}}", str(data[param]))
                # Remove from data so it's not included in request body
                del data[param]
        
        return base_url + url

    @staticmethod
    def get_available_tools(category=None):
        """
        Get list of available tools
        """
        if category:
            tools = ToolsRegistry.get_tools_by_category(category)
        else:
            tools = ToolsRegistry.get_all_tools()

        return {
            "tools": list(tools.keys()),
            "count": len(tools),
            "category": category
        }
