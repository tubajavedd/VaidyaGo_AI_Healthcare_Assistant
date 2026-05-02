# Vado AI Chatbot - Complete API Tool Integration

This document explains how the chatbot now integrates with all APIs in the vaidyaGo system.

## Architecture Overview

```
User Input
    ↓
PromptService (adds tools context)
    ↓
LLMService (multi-backend support)
    ↓
MistralService (ensures JSON response)
    ↓
IntentService (parses intent and action)
    ↓
ToolRouter (executes the requested action)
    ↓
API Call or Direct Response
    ↓
Response to User
```

## Features

### 1. **Multi-Backend LLM Support**
The chatbot now supports multiple LLM backends with automatic fallback:
- **Local TinyLlama Model** - Uses cached model in `hf_cache/` folder
- **OpenAI API** - If OPENAI_API_KEY is configured
- **HuggingFace Inference API** - Your existing setup
- **Fallback Mode** - Simple JSON parsing when all else fails

### 2. **Unified Tool/API Registry**
All available APIs are registered in `tools_registry.py`. The system automatically discovers and uses them.

**Available Tool Categories:**
- Appointments (book, cancel, reschedule, list)
- Doctor Slots (get available, generate)
- Documents (upload, retrieve)
- Feedback (submit)
- Prescriptions (get, request)
- Medications (add past medication, get schedule)
- Authentication (send/verify OTP)
- Notifications (get, mark read)
- Reminders (set, get)
- Payments (make, get history)
- User Profile (get, update)

### 3. **Smart Tool Execution**
The `ToolRouter` automatically executes any registered tool based on user intent:
- Parses user intent from LLM response
- Validates tool exists
- Calls the appropriate API endpoint
- Returns formatted response

## API Endpoints

### 1. Chat Endpoint
```
POST /api/vado/chat/
Body: {"message": "Book an appointment with Dr. Smith"}
Response: {
    "success": true,
    "message": "Appointment booked successfully",
    "intent": "book_appointment",
    "action": "book_appointment",
    "data": {...},
    "action_executed": true
}
```

### 2. Available Tools Endpoint
```
GET /api/vado/tools/
GET /api/vado/tools/?category=appointments
Response: {
    "success": true,
    "tools": {
        "tools": ["book_appointment", "cancel_appointment", ...],
        "count": 30,
        "category": "appointments"
    },
    "categories": ["appointments", "prescriptions", ...]
}
```

### 3. Tools Description Endpoint
```
GET /api/vado/tools-description/
Response: {
    "success": true,
    "tools": {
        "appointments": [
            {
                "name": "book_appointment",
                "description": "Book a medical appointment with a doctor"
            },
            ...
        ],
        ...
    },
    "total_tools": 30,
    "categories": ["appointments", "prescriptions", ...]
}
```

## How to Use

### For Users
Users can now interact with the chatbot naturally:
```
User: "Book an appointment with Dr. Smith on Monday at 10 AM"
Chatbot: "Processing your request..."
Response: "Appointment booked successfully"
```

### For Developers

#### Adding a New API to the Chatbot

1. **Add tool definition in `tools_registry.py`:**
```python
TOOLS_REGISTRY = {
    "my_new_tool": {
        "name": "my_new_tool",
        "description": "Description of what this tool does",
        "category": "category_name",
        "endpoint": "/api/my-endpoint/",
        "method": "POST",
        "parameters": {
            "param1": {"type": "string", "description": "Description"},
            "param2": {"type": "integer", "description": "Description"}
        },
        "response_format": {
            "success": True,
            "message": "Tool executed"
        }
    }
}
```

2. **The rest is automatic!** The chatbot will:
   - Include this tool in the LLM system prompt
   - Allow users to request this action
   - Execute the API call automatically

#### Configuring LLM Backend

Edit `.env` file:
```env
# For local model (automatic)
# Set HF_API_KEY if you want HuggingFace support
HF_API_KEY=your_hf_key

# For OpenAI support (optional)
OPENAI_API_KEY=your_openai_key
```

## Response Format

### Tool Execution Response
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "intent": "book_appointment",
    "action": "book_appointment",
    "data": {
        "appointment_id": 123,
        "doctor": "Dr. Smith",
        "date": "2026-05-05",
        "time": "10:00"
    },
    "action_executed": true
}
```

### Error Response
```json
{
    "success": false,
    "error": "Error message",
    "message": "I encountered an error",
    "action_executed": false
}
```

## LLM Response Format (What the LLM should return)

The LLM is instructed to return responses in this JSON format:
```json
{
    "intent": "book_appointment",
    "action": "book_appointment",
    "message": "I'll help you book an appointment",
    "data": {
        "doctor_id": 123,
        "date": "2026-05-05",
        "time": "10:00"
    },
    "confidence": 0.95
}
```

## Database Integration

Chat messages are automatically stored in the `ChatMessage` model:
- `user` - Username of the user
- `message` - Original user message
- `response` - AI response message
- `created_at` - Timestamp

## Configuration

### Base URL for API Calls
Edit `tool_router.py` to set the correct base URL:
```python
base_url = "http://localhost:8000"  # Change for production
```

### Timeout
Default API timeout: 30 seconds
Edit in `llm_service.py` and `tool_router.py`

## Troubleshooting

### Error: "LLM request failed: 404"
This is now automatically handled! The system will:
1. Try local TinyLlama model
2. Fall back to OpenAI if configured
3. Fall back to HuggingFace with retry logic
4. Use fallback JSON parsing mode

### Tool Not Executing
1. Check if tool is registered in `tools_registry.py`
2. Verify endpoint URL is correct
3. Check user authentication
4. Review logs in `chatbot/services/tool_router.py`

### LLM Not Generating Proper JSON
The system has fallback logic that automatically handles:
- Plain text responses (converts to JSON)
- Malformed JSON (attempts parsing)
- Missing actions (treats as chat)

## Performance Tips

1. **Use Local Model** - Fastest, runs on-device
   - Download model: `python -c "from transformers import pipeline; pipeline('text-generation', model='TinyLlama/TinyLlama-1.1B-Chat-v1.0')"`

2. **Cache LLM Responses** - Add caching layer
   ```python
   from django.views.decorators.cache import cache_page
   @cache_page(60 * 5)  # Cache for 5 minutes
   ```

3. **Async Tool Execution** - For long-running tools
   ```python
   from celery import shared_task
   @shared_task
   def execute_tool_async(action, data):
       # Long-running operation
   ```

## Security Considerations

1. **Authentication** - Tools respect user authentication
2. **Authorization** - Each API endpoint has its own permissions
3. **Input Validation** - Tool parameters are validated before execution
4. **API Keys** - Stored in environment variables, not in code

## Future Enhancements

- [ ] Streaming responses for long operations
- [ ] Tool chaining (multiple API calls)
- [ ] Natural language response generation
- [ ] Context memory and conversation history
- [ ] User feedback and learning
- [ ] Analytics and usage tracking
- [ ] Tool usage analytics
- [ ] A/B testing different LLM prompts
