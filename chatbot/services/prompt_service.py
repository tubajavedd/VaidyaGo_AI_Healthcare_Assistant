from chatbot.services.tools_registry import ToolsRegistry


class PromptService:
    """
    Central service to build prompts for LLM (Vado AI assistant)
    """

    SYSTEM_PROMPT = """You are Vado AI assistant - a helpful healthcare medical assistant. You help users with healthcare-related queries and can execute various medical and appointment-related tasks.

CORE RULES:
- Be polite, friendly, and professional
- Give short, clear, and accurate answers
- Do NOT give harmful or unsafe medical advice
- If unsure about medical conditions, always suggest consulting a real doctor
- Keep responses simple and easy to understand
- Use available tools/APIs to help users with their requests
- IMPORTANT: When extracting data for appointment booking, extract as much info as possible from the user's message:
  - If user mentions a doctor (e.g., "Dr. Smith", "with Dr. Smith"), extract as "doctor_name": "Smith"
  - If user mentions a day (e.g., "Monday", "next Monday"), extract as "day_name": "monday" or convert to date
  - If user mentions time (e.g., "10 AM", "10:00"), extract as "time": "10:00"
  - Do NOT require slot ID - the system can auto-resolve slot from doctor + date + time

RESPONSE FORMAT:
Always respond in JSON format with this structure:
{
    "intent": "string (one of: book_appointment, cancel_appointment, reschedule_appointment, get_appointments, get_slots, feedback, prescription, medication, reminder, notification, payment, profile, chat)",
    "action": "string (name of the tool to execute, if any)",
    "message": "string (your response to the user)",
    "data": {
        // Include parameters needed for the action here
        // See AVAILABLE TOOLS below for required parameters
    },
    "confidence": 0.0 to 1.0 (your confidence in understanding the user's intent)
}

AVAILABLE TOOLS AND ACTIONS:
You have access to the following tools/APIs. When user requests match these actions, include the action name and required parameters in your response."""

    @staticmethod
    def get_tools_description():
        """Get formatted description of all available tools"""
        summary = ToolsRegistry.get_tools_summary()
        description = ""

        for category, tools in summary.items():
            description += f"\n{category.upper()}:\n"
            for tool in tools:
                description += f"  - {tool['name']}: {tool['description']}\n"

        return description

    @staticmethod
    def build_prompt(message, memory=None, history=None):
        """
        Build final prompt for LLM with tools information
        """

        memory = memory if memory else "No memory available."
        history = history if history else "No conversation history."
        tools_desc = PromptService.get_tools_description()

        prompt = f"""{PromptService.SYSTEM_PROMPT}
{tools_desc}

--- CONVERSATION CONTEXT ---
Memory:
{memory}

Chat History:
{history}

--- USER MESSAGE ---
{message}

--- INSTRUCTIONS ---
1. Understand what the user is asking
2. If it's a general query, respond as the AI assistant
3. If it matches one of the available tools/actions, set the "action" field and include required parameters in "data"
4. Always respond in valid JSON format
5. Be helpful and clear
"""
        return prompt
