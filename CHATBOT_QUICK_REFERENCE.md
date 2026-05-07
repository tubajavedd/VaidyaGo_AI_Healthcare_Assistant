# Quick Reference: Chatbot API Integration

## Upload Document via Chatbot

### Option 1: Via Chat Endpoint with Document
```python
import requests

url = "http://localhost:8000/api/chatbot/chat/"
headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}

# Send message with document
files = {
    "document": open("prescription.pdf", "rb")
}
data = {
    "message": "Please help me understand this prescription"
}

response = requests.post(url, files=files, data=data, headers=headers)
print(response.json())
```

### Option 2: Via Dedicated Upload Endpoint
```python
import requests

url = "http://localhost:8000/api/chatbot/upload-prescription/"
headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}

files = {
    "document": open("prescription.pdf", "rb")
}

response = requests.post(url, files=files, headers=headers)
result = response.json()
print(f"Prescription ID: {result['prescriptions'][0]['prescription_id']}")
print(f"Doctor: {result['prescriptions'][0]['doctor_name']}")
print(f"Medicines: {result['prescriptions'][0]['medicines']}")
```

## Retrieve Prescription Information

### Get All Prescriptions
```python
import requests

url = "http://localhost:8000/api/chatbot/prescriptions/list/"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

response = requests.get(url, headers=headers)
prescriptions = response.json()["prescriptions"]

for rx in prescriptions:
    print(f"ID: {rx['id']}, Doctor: {rx['doctor_name']}, Medicines: {rx['medicines_count']}")
```

### Get Prescription Details
```python
import requests

rx_id = 1
url = f"http://localhost:8000/api/chatbot/prescriptions/{rx_id}/details/"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

response = requests.get(url, headers=headers)
rx_data = response.json()["prescription"]

print(f"Doctor: {rx_data['doctor_name']}")
print(f"Hospital: {rx_data['hospital_name']}")
print(f"Date: {rx_data['prescription_date']}")
print(f"Medicines: {len(rx_data['medicines'])}")
```

### Get Medicines from Prescription
```python
import requests

rx_id = 1
url = f"http://localhost:8000/api/chatbot/prescriptions/{rx_id}/medicines/"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

response = requests.get(url, headers=headers)
medicines = response.json()["medicines"]

for med in medicines:
    print(f"{med['name']} - {med['dosage']} {med['frequency']} for {med['duration_days']} days")
    print(f"Instructions: {med['instructions']}\n")
```

## Chat with Chatbot About APIs

### Ask What Vado Can Do
```
User: "What can you help me with?"
Vado: "I can help you with:
       - Book and manage appointments
       - View and understand prescriptions
       - Manage your medicines and reminders
       - Check lab results
       - And much more! What do you need?"
```

### Get Information About Available APIs
```
GET /api/chatbot/all-apis/

Response includes:
- Total API count
- API categories
- Detailed API information (endpoint, method, parameters)
- Response format for each API
```

### Upload Document and Get Analysis
```
User: "I uploaded my lab report. Can you explain the results?"
[Uploads lab_report.pdf]
Chatbot: "✅ I've analyzed your lab report! Here's what I found:
          - Test Name: Blood Glucose
            Result: 110 mg/dL
            Reference: 70-100 mg/dL
            Status: High
          
          I recommend consulting with your doctor about these findings."
```

## Chatbot Intent Examples

### Intent: Upload Prescription
```json
{
    "intent": "upload_prescription",
    "action": "upload_prescription_document",
    "message": "I've extracted your prescription",
    "data": {
        "prescription_id": 1,
        "medicines": [...]
    },
    "action_executed": true
}
```

### Intent: Book Appointment
```json
{
    "intent": "book_appointment",
    "action": "book_appointment",
    "message": "Let me book that appointment for you",
    "data": {
        "doctor_name": "Dr. Smith",
        "date": "2026-05-10",
        "time": "10:00"
    },
    "action_executed": true
}
```

### Intent: General Chat
```json
{
    "intent": "chat",
    "action": null,
    "message": "Here's the information you requested...",
    "data": {},
    "action_executed": false
}
```

## Available Tool Categories

| Category | Examples | Use Case |
|----------|----------|----------|
| **appointments** | book, cancel, reschedule, list | Manage doctor visits |
| **medications** | get_prescriptions, add_past_medication | Medicine management |
| **prescriptions** | upload_document, extract_medicines | Handle medical docs |
| **reminders** | set_reminder, get_reminders | Medicine/appointment reminders |
| **payments** | make_payment, get_history | Payment management |
| **profile** | get_profile, update_profile | User profile |
| **notifications** | get_notifications, mark_read | View notifications |

## Error Handling

```python
import requests

try:
    url = "http://localhost:8000/api/chatbot/upload-prescription/"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    files = {"document": open("file.pdf", "rb")}
    
    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    if result['success']:
        print("Upload successful")
        for rx in result['prescriptions']:
            if rx['status'] == 'success':
                print(f"Extracted prescription {rx['prescription_id']}")
            else:
                print(f"Error: {rx['message']}")
    else:
        print(f"Upload failed: {result.get('error')}")
        
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication required. Please provide valid token.")
    elif e.response.status_code == 400:
        print("Invalid request. Check file format and parameters.")
    else:
        print(f"HTTP Error: {e}")
        
except Exception as e:
    print(f"Error: {str(e)}")
```

## Testing Endpoints

### Using cURL

```bash
# Get all APIs
curl http://localhost:8000/api/chatbot/all-apis/

# Get tools description
curl http://localhost:8000/api/chatbot/tools-description/

# Upload prescription (requires auth)
curl -X POST http://localhost:8000/api/chatbot/upload-prescription/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "document=@prescription.pdf"

# Send chat message with document
curl -X POST http://localhost:8000/api/chatbot/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "message=Help with this prescription" \
  -F "document=@prescription.pdf"

# Get prescriptions list
curl http://localhost:8000/api/chatbot/prescriptions/list/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get prescription details
curl http://localhost:8000/api/chatbot/prescriptions/1/details/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Key Features Summary

✅ **Document Upload** - Upload prescriptions, lab reports, scans  
✅ **Auto-Extraction** - Automatic data extraction via OCR  
✅ **API Discovery** - Complete API catalog accessible  
✅ **40+ APIs** - Access entire VaidyaGo platform via chatbot  
✅ **Smart Routing** - LLM intelligently selects appropriate API  
✅ **Multi-format** - Supports images, PDFs, documents  
✅ **Auto-Scheduling** - Automatic medicine schedule creation  
✅ **Data Extraction** - Medicines, test results, findings, recommendations

---

For complete documentation, see: `CHATBOT_API_INTEGRATION_GUIDE.md`
