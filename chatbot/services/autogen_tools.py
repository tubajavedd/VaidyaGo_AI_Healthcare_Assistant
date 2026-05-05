"""
AutoGen Tool Integration for VaidyaGo.

This module provides AutoGen-compatible tool definitions that wrap
the VaidyaGo backend APIs through ToolRouter.
"""

import json
import logging
from typing import Any, Dict

from chatbot.services.tool_router import ToolRouter

logger = logging.getLogger(__name__)


class AutoGenToolWrapper:
    """
    Wraps VaidyaGo tools for AutoGen agent usage.
    """

    @staticmethod
    def get_tool_definitions():
        """
        Get AutoGen-compatible tool definitions.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "book_appointment",
                    "description": "Book an appointment with a doctor",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_name": {
                                "type": "string",
                                "description": "Name of the doctor"
                            },
                            "date": {
                                "type": "string",
                                "description": "Appointment date (YYYY-MM-DD or day name)"
                            },
                            "time": {
                                "type": "string",
                                "description": "Appointment time (HH:MM format)"
                            },
                            "patient_name": {
                                "type": "string",
                                "description": "Patient name (auto-filled if not provided)"
                            },
                            "patient_phone": {
                                "type": "string",
                                "description": "Patient phone (auto-filled if not provided)"
                            },
                        },
                        "required": ["doctor_name", "date", "time"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_doctor_slots",
                    "description": "Get available doctor appointment slots",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_name": {
                                "type": "string",
                                "description": "Doctor name"
                            },
                            "date": {
                                "type": "string",
                                "description": "Appointment date (optional)"
                            },
                        },
                        "required": ["doctor_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "cancel_appointment",
                    "description": "Cancel an existing appointment",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "Appointment ID to cancel"
                            },
                        },
                        "required": ["appointment_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "list_appointments",
                    "description": "List user's appointments",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
        ]

    @staticmethod
    def execute_tool(tool_name: str, tool_input: Dict[str, Any], user: Any = None):
        """
        Execute a tool through ToolRouter.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool
            user: Django user object (optional)
        
        Returns:
            Tool execution result
        """
        intent_data = {
            "action": tool_name,
            "intent": tool_name,
            "message": f"Executing {tool_name}...",
            "data": tool_input,
        }

        try:
            result = ToolRouter.execute(intent_data, user)
            logger.info(f"Tool executed: {tool_name} -> {result.get('action_executed')}")
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {tool_name} - {str(e)}")
            return {
                "message": f"Failed to execute {tool_name}: {str(e)}",
                "action_executed": False,
                "data": {},
            }

    @staticmethod
    def process_autogen_tool_call(tool_name: str, tool_input: str, user: Any = None):
        """
        Process an AutoGen tool call (usually JSON string input).
        
        Args:
            tool_name: Name of the tool
            tool_input: JSON string with tool parameters
            user: Django user object
        
        Returns:
            Processed result as JSON string
        """
        try:
            input_dict = json.loads(tool_input) if isinstance(tool_input, str) else tool_input
            result = AutoGenToolWrapper.execute_tool(tool_name, input_dict, user)
            return json.dumps(result)
        except json.JSONDecodeError:
            return json.dumps({
                "message": f"Invalid tool input for {tool_name}",
                "action_executed": False,
                "data": {},
            })
        except Exception as e:
            logger.error(f"Tool call processing failed: {str(e)}")
            return json.dumps({
                "message": f"Error processing tool call: {str(e)}",
                "action_executed": False,
                "data": {},
            })
