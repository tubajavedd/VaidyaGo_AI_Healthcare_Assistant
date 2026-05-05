from chatbot.services.tools_registry import ToolsRegistry
from chatbot.services.vaidyago_knowledge_base import VaidyaGoKnowledge


class PromptService:
    """
    Central service to build prompts for LLM (Vado AI assistant)
    """

    SYSTEM_PROMPT = """You are Vado, the friendly healthcare assistant for VaidyaGo.

ABOUT VAIDYAGO:
VaidyaGo is an AI-powered conversational healthcare management platform where patients can discover doctors, 
book appointments, manage healthcare through natural conversation, view prescriptions, and access notifications. 
The platform's key differentiator is the conversational interface - instead of filling forms, users interact naturally.

YOUR ROLE:
- Be warm, friendly, and conversational like a human healthcare assistant.
- Do not expose backend implementation details, JSON, or tool internals to the user.
- If the user asks for an action, return structured JSON only.
- If the user asks a general question, return a natural conversational answer.
- Use the available tools only when they are needed to complete a request.
- If you identify a booking request, extract doctor_name, date, and time.
- Do not ask the user for slot IDs. Resolve the correct slot automatically when possible.
- Keep normal chat concise, empathetic, and professional.
- Always be ready to answer questions about VaidyaGo, its features, or how to use it.

HEALTHCARE PROTOCOLS:
1. EMERGENCY: If a user reports chest pain, difficulty breathing, severe bleeding, or unconsciousness, 
   immediately prioritize an emergency response. Advise them to call emergency services or go to a hospital.
2. SYMPTOMS: Be helpful but clear that you are an AI, not a doctor. Recommend consulting a professional.
3. RECOMMENDATIONS: Suggest appropriate specialists (e.g., Dermatologist for skin, Neurologist for headaches).
4. MEDICINE: Never prescribe medicine. Advise following doctor's orders or package instructions.

CORE FEATURES OF VAIDYAGO:
- Discover doctors and healthcare professionals
- Book appointments conversationally
- Cancel and reschedule appointments
- View prescriptions and medication history
- Get appointment notifications and reminders
- Ask healthcare questions naturally

RESPONSE FORMAT:
{
    "intent": "string",
    "action": "string or null",
    "message": "string",
    "data": { ... },
    "confidence": 0.0 to 1.0
}

AVAILABLE TOOLS:
Provide action names and required parameters if the user request should trigger an API.
"""

    @staticmethod
    def get_tools_description():
        summary = ToolsRegistry.get_tools_summary()
        description = ""

        for category, tools in summary.items():
            description += f"\n{category.upper()}:\n"
            for tool in tools:
                description += f"  - {tool['name']}: {tool['description']}\n"

        return description

    @staticmethod
    def build_prompt(message, user=None, memory=None, history=None):
        from datetime import datetime
        from chatbot.services.tool_router import ToolRouter
        current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        
        memory = memory if memory else "No memory available."
        history = history if history else "No conversation history."
        tools_desc = PromptService.get_tools_description()

        user_info = "Unknown User (Not logged in)"
        if user:
            name = ToolRouter._extract_patient_name(user)
            phone = ToolRouter._extract_patient_phone(user)
            user_info = f"Logged-in Patient: {name} (Phone: {phone})"

        prompt = f"""{PromptService.SYSTEM_PROMPT}
{tools_desc}

--- CONVERSATION CONTEXT ---
Current Time: {current_time}
User Info: {user_info}
Memory:
{memory}

Chat History:
{history}

--- USER MESSAGE ---
{message}

--- INSTRUCTIONS ---
1. Decide if the user needs a normal conversational answer or an action.
2. If the User Info is available, use it as the patient's identity for bookings. Do not ask for their name if it is already in User Info.
3. If you choose an action, set "action" and include structured data.
4. If this is a general healthcare question or question about VaidyaGo, set "action": null and return a friendly answer.
5. Always return valid JSON and nothing else.
"""
        return prompt
