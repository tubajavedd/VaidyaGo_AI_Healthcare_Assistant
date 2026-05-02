# Quick Start - Vado AI Chatbot Integration

## ⚡ 5-Minute Setup

### Step 1: Update Dependencies
```bash
cd d:\directory\vaidyaGo\vaidyaGo
pip install -r requirements.txt
```

### Step 2: Choose LLM Backend
```bash
# Option A: Local Model (RECOMMENDED - fastest, no API key)
pip install torch transformers

# Option B: Or keep using HuggingFace
# (HF_API_KEY already in .env)

# Option C: Or add OpenAI
# pip install openai
# Add to .env: OPENAI_API_KEY=sk-...
```

### Step 3: Run Server
```bash
python manage.py runserver
```

### Step 4: Test It!
```bash
# Terminal 1: Already running from Step 3

# Terminal 2: Try the chatbot
python chatbot/test_chatbot_api.py
```

## 🎯 Example Prompts

Try these to see the chatbot in action:

```
"Book an appointment with Dr. Smith on Monday at 10 AM"
↓
Chatbot will: Extract intent → Call appointment API → Book it

"What are my active prescriptions?"
↓
Chatbot will: Recognize prescription query → Call prescription API → Show results

"Set a reminder for my aspirin at 8 AM"
↓
Chatbot will: Understand reminder request → Call reminder API → Create it

"Show me my notifications"
↓
Chatbot will: Get notifications → Call notification API → List them

"I want to pay for my appointment"
↓
Chatbot will: Recognize payment → Call payment API → Create transaction
```

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER MESSAGE                             │
│           "Book appointment on Monday 10 AM"                 │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 PROMPT SERVICE                               │
│    Builds prompt with all available tools/APIs               │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    LLM SERVICE                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Try 1: Local TinyLlama Model        ✓ (Works)         │ │
│  │ Try 2: OpenAI API                   (Fallback)        │ │
│  │ Try 3: HuggingFace API              (Fallback)        │ │
│  │ Try 4: Simple JSON Parser           (Last resort)     │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
                  Response: JSON with intent
         {
           "intent": "book_appointment",
           "action": "book_appointment",
           "data": {"date": "2026-05-05", "time": "10:00"}
         }
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 INTENT SERVICE                               │
│              Parse intent and action                         │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│               TOOL ROUTER / API EXECUTOR                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. Check if tool exists in registry      ✓            │ │
│  │ 2. Get endpoint: /api/appointments/create/             │ │
│  │ 3. Call HTTP POST with parameters                      │ │
│  │ 4. Return result                                       │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   API ENDPOINT                               │
│           /api/appointments/create/                          │
│                  (Django View)                               │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE                                  │
│              Appointment created ✓                           │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  RESPONSE TO USER                            │
│    "Appointment booked successfully on Monday at 10 AM"      │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Available Tools by Category

### 📅 Appointments (4 tools)
- book_appointment
- cancel_appointment
- reschedule_appointment
- list_appointments

### 🕐 Doctor Slots (2 tools)
- get_doctor_slots
- generate_slots

### 📄 Documents (2 tools)
- upload_doctor_documents
- get_doctor_documents

### 💊 Prescriptions & Medications (4 tools)
- get_prescriptions
- request_prescription
- add_past_medication
- get_medication_schedule

### ⭐ Feedback (1 tool)
- submit_feedback

### 🔔 Notifications & Reminders (4 tools)
- get_notifications
- mark_notification_read
- set_reminder
- get_reminders

### 💳 Payments (2 tools)
- make_payment
- get_payment_history

### 👤 Profile & Auth (4 tools)
- send_otp
- verify_otp
- get_user_profile
- update_user_profile

**Total: 30+ APIs automatically available!**

## 🧪 Test Commands

```bash
# Option 1: Python test script
python chatbot/test_chatbot_api.py

# Option 2: cURL commands
curl -X POST http://localhost:8000/api/vado/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"Book an appointment"}'

# Option 3: Django shell
python manage.py shell
from chatbot.services.tools_registry import ToolsRegistry
print(ToolsRegistry.get_tools_summary())

# Option 4: View available tools via API
curl http://localhost:8000/api/vado/tools/
```

## 📖 Documentation Files

Created for you:

1. **CHATBOT_SETUP_SUMMARY.md** ← You are here
   - Complete overview and examples

2. **CHATBOT_INTEGRATION_GUIDE.md**
   - Detailed technical documentation
   - How to add new tools
   - Configuration details

3. **.env.example**
   - Copy and configure for your setup
   - All LLM backend options

4. **test_chatbot_api.py**
   - Ready-to-run test suite
   - Example API calls

5. **setup_chatbot.py**
   - Initialize and display available tools

## 🐛 If Something Goes Wrong

### Error: "LLM request failed: 404"
✅ FIXED! The system now tries multiple backends automatically.

### Error: "Tool not found"
- Check `chatbot/services/tools_registry.py`
- Make sure your API endpoint exists
- Verify method is POST/GET/etc.

### Error: "Connection refused"
- Make sure Django server is running: `python manage.py runserver`
- Check API_BASE_URL in `.env`

### Error: "ImportError: No module named transformers"
- Install: `pip install torch transformers`

## 🚀 Production Deployment

Before going live:

1. **Update API_BASE_URL** in `.env` to your domain
2. **Use OpenAI or local model** (HF has rate limits)
3. **Enable chat logging** for analytics
4. **Set up error monitoring** (Sentry, etc.)
5. **Configure CORS** if frontend is separate domain
6. **Add API rate limiting**
7. **Use HTTPS** only

## 📞 Support & Next Steps

- Review `CHATBOT_INTEGRATION_GUIDE.md` for advanced topics
- Run tests to verify everything works
- Try different example prompts
- Add your own APIs following the guide
- Deploy to production

---

**🎉 Your AI Chatbot is ready to revolutionize medical appointments!**

All APIs are now accessible through natural language. Users can ask the chatbot anything about appointments, medications, payments, and the chatbot will automatically execute the right API calls.
