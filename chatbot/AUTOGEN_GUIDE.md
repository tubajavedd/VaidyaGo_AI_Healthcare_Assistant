# AutoGen Integration for VaidyaGo Chatbot

This document explains how to enable and use AutoGen multi-agent framework with the VaidyaGo chatbot system.

## What is AutoGen?

AutoGen is a framework for building multi-agent conversations with Large Language Models (LLMs). It allows:
- Multiple agents to collaborate on complex tasks
- Agents to call functions/tools
- Natural conversation flows with LLM-powered decision making

## Prerequisites

1. **Mistral API Key** - Required for AutoGen to work with Mistral models
   ```bash
   export MISTRAL_API_KEY="your_mistral_api_key_here"
   export MISTRAL_MODEL="mistral-large"  # optional, defaults to mistral-large
   ```

2. **Python packages** - Already added to `requirements.txt`:
   ```bash
   pip install pyautogen
   ```

## Enabling AutoGen

### Option 1: Environment Variable
```bash
# In your .env file or shell environment
export CHATBOT_USE_AUTOGEN=true
```

### Option 2: Programmatically
```python
from chatbot.services.autogen_config import enable_autogen
enable_autogen()
```

### Option 3: Check Status
```python
from chatbot.services.autogen_config import validate_autogen_setup
status = validate_autogen_setup()
print(status)
# Output:
# {
#     'valid': True,
#     'issues': [],
#     'autogen_enabled': True,
#     'mistral_configured': True
# }
```

## Architecture

When AutoGen is enabled:

```
User Request
    ↓
ChatbotEngine
    ↓
IntentService (parse LLM output)
    ↓
AgentManager
    ├─→ If USE_AUTOGEN=true:
    │   └─→ AssistantAgent (Vado)
    │       ↓
    │       UserProxyAgent
    │       ↓
    │       Tool Execution (through ToolRouter)
    │
    └─→ If USE_AUTOGEN=false (default):
        └─→ ToolRouter (direct execution)
```

## Available Tools in AutoGen Mode

AutoGen agents can call these tools automatically:

1. **book_appointment** - Schedule an appointment
   - `doctor_name` (required)
   - `date` (required): YYYY-MM-DD or day name
   - `time` (required): HH:MM format
   - `patient_name`, `patient_phone` (optional)

2. **get_doctor_slots** - Check available slots
   - `doctor_name` (required)
   - `date` (optional)

3. **cancel_appointment** - Cancel an appointment
   - `appointment_id` (required)

4. **list_appointments** - Show user's appointments

## Example Usage

### With AutoGen Enabled

```bash
# Set up environment
export CHATBOT_USE_AUTOGEN=true
export MISTRAL_API_KEY="your_key_here"

# Start Django
python manage.py runserver
```

### Test in Postman

```
POST http://127.0.0.1:8000/api/vado/chat/

{
  "message": "Book an appointment with Dr Smith on Monday at 10 AM"
}
```

**Response (with AutoGen):**
```json
{
  "success": true,
  "reply": "I've successfully booked your appointment with Dr. Smith for Monday at 10:00 AM.",
  "intent": "book_appointment",
  "action": "book_appointment",
  "data": {
    "appointment_id": 123,
    "doctor_id": 45,
    "slot_id": 678
  },
  "action_executed": true
}
```

## Configuration Files

### `autogen_config.py`
Provides helper functions for AutoGen setup:
- `get_autogen_config()` - Get LLM configuration
- `enable_autogen()` - Enable AutoGen mode
- `disable_autogen()` - Disable AutoGen mode
- `is_autogen_enabled()` - Check if enabled
- `validate_autogen_setup()` - Validate configuration

### `autogen_tools.py`
Wraps backend tools for AutoGen:
- `AutoGenToolWrapper.get_tool_definitions()` - Get tool specs
- `AutoGenToolWrapper.execute_tool()` - Execute a tool
- `AutoGenToolWrapper.process_autogen_tool_call()` - Process tool calls

### `agent_manager.py`
Main agent routing logic:
- `AgentManager.handle()` - Route intents to agent or tool router
- `AgentManager._handle_with_autogen()` - Use AutoGen for execution
- `AgentManager.get_autogen_status()` - Get current status

## Fallback Behavior

If AutoGen fails for any reason:
1. Logs the error with reason
2. Automatically falls back to direct `ToolRouter` execution
3. Request completes successfully without user seeing the error

## Performance Notes

- **AutoGen Mode**: Slightly slower (extra LLM calls) but more intelligent
- **Direct Mode** (default): Faster, more predictable
- Both modes return identical response format

## Troubleshooting

### AutoGen not executing

```python
from chatbot.services.agent_manager import AgentManager
status = AgentManager.get_autogen_status()
print(status)
```

Check:
- `autogen_enabled` is `True`
- `mistral_api_key_set` is `True`
- No errors in Django logs

### Tool calls failing

Check:
1. Doctor exists in database
2. Slots are available
3. Date/time format is correct (YYYY-MM-DD, HH:MM)
4. User is authenticated (for some operations)

### LLM Not Responding

Ensure:
- `MISTRAL_API_KEY` is valid
- Network connection is working
- Mistral API is accessible
- Model name is correct

## Future Enhancements

- [ ] Group Chat with multiple agents (e.g., Vado + Doctor recommendation agent)
- [ ] Persistent conversation state in AutoGen
- [ ] Custom tool definitions from admin panel
- [ ] Agent performance monitoring
- [ ] Support for other LLM providers (OpenAI, Anthropic)

## References

- AutoGen Documentation: https://microsoft.github.io/autogen/
- Mistral API Docs: https://docs.mistral.ai/
- VaidyaGo Chatbot Architecture: See `chatbot/` directory
