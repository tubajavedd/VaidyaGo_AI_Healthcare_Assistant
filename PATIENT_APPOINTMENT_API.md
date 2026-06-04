# 👤 Patient Appointment API Documentation

## Overview
The Patient Appointment API allows authenticated patients/users to view their appointments with detailed doctor information. Patients can see all their appointments, filter by status, and view complete appointment details including the doctor they will be consulting.

---

## Base URL
```
http://localhost:8000/api/appointments
```

---

## Authentication
All patient endpoints require **JWT Authentication**.

### Headers Required:
```
Authorization: Bearer <your_jwt_token>
```

### Getting JWT Token:
1. Sign up or login at `/auth/signup/` or `/auth/login/`
2. Use the token returned in the response

---

## 📋 Endpoints

### 1. **Get All Patient Appointments**
Retrieve all appointments for the authenticated patient.

#### Endpoint:
```
GET /patient/appointments/
```

#### Headers:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Query Parameters (Optional):
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `status` | string | Filter by appointment status | `pending`, `confirmed`, `booked`, `cancelled`, `rejected`, `outpatient` |
| `date_from` | string | Filter appointments from date (YYYY-MM-DD) | `2025-01-15` |
| `date_to` | string | Filter appointments until date (YYYY-MM-DD) | `2025-12-31` |

#### Example Requests:

**Get all appointments:**
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/" \
  -H "Authorization: Bearer your_token_here"
```

**Get confirmed appointments only:**
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/?status=confirmed" \
  -H "Authorization: Bearer your_token_here"
```

**Get appointments from a date range:**
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/?date_from=2025-01-01&date_to=2025-12-31" \
  -H "Authorization: Bearer your_token_here"
```

#### Success Response (200 OK):
```json
{
  "message": "Appointments retrieved successfully",
  "count": 3,
  "appointments": [
    {
      "id": 1,
      "doctor_details": {
        "id": 5,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "mobile_number": "9876543210",
        "alternate_number": "9123456789",
        "email": "john.doe@medical.com",
        "city": "Mumbai",
        "address": "123 Medical Plaza, Floor 5",
        "gender": "male"
      },
      "slot": 12,
      "slot_details": {
        "id": 12,
        "doctor": 5,
        "start_time": "2025-01-20T10:00:00Z",
        "end_time": "2025-01-20T10:30:00Z",
        "is_booked": true,
        "slot_duration": 30
      },
      "patient_name": "Jane Smith",
      "patient_phone": "9988776655",
      "patient_email": "jane.smith@email.com",
      "patient_age": 35,
      "patient_gender": "female",
      "patient_mrn": "MRN-12345",
      "patient_weight": "65kg",
      "patient_disease": "Hypertension",
      "patient_heart_rate": "75 bpm",
      "patient_blood_type": "O+",
      "patient_photo": null,
      "appointment_type": "Follow-up Consultation",
      "location": "Room 501",
      "start_time": "2025-01-20T10:00:00Z",
      "end_time": "2025-01-20T10:30:00Z",
      "status": "confirmed",
      "reschedule_reason": null,
      "rejection_reason": null,
      "created_at": "2025-01-15T14:30:00Z"
    }
  ]
}
```

#### Error Response (401 Unauthorized):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Error Response (400 Bad Request - Invalid Date):
```json
{
  "error": "Invalid date format for date_from. Use YYYY-MM-DD"
}
```

---

### 2. **Get Specific Appointment Details**
Retrieve detailed information about a specific appointment.

#### Endpoint:
```
GET /patient/appointments/<appointment_id>/
```

#### Path Parameters:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `appointment_id` | integer | Yes | The ID of the appointment to retrieve |

#### Headers:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Example Request:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/1/" \
  -H "Authorization: Bearer your_token_here"
```

#### Success Response (200 OK):
```json
{
  "message": "Appointment details retrieved successfully",
  "appointment": {
    "id": 1,
    "doctor_details": {
      "id": 5,
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "mobile_number": "9876543210",
      "alternate_number": "9123456789",
      "email": "john.doe@medical.com",
      "city": "Mumbai",
      "address": "123 Medical Plaza, Floor 5",
      "gender": "male"
    },
    "slot": 12,
    "slot_details": {
      "id": 12,
      "doctor": 5,
      "start_time": "2025-01-20T10:00:00Z",
      "end_time": "2025-01-20T10:30:00Z",
      "is_booked": true,
      "slot_duration": 30
    },
    "patient_name": "Jane Smith",
    "patient_phone": "9988776655",
    "patient_email": "jane.smith@email.com",
    "patient_age": 35,
    "patient_gender": "female",
    "patient_mrn": "MRN-12345",
    "patient_weight": "65kg",
    "patient_disease": "Hypertension",
    "patient_heart_rate": "75 bpm",
    "patient_blood_type": "O+",
    "patient_photo": null,
    "appointment_type": "Follow-up Consultation",
    "location": "Room 501",
    "start_time": "2025-01-20T10:00:00Z",
    "end_time": "2025-01-20T10:30:00Z",
    "status": "confirmed",
    "reschedule_reason": null,
    "rejection_reason": null,
    "created_at": "2025-01-15T14:30:00Z"
  }
}
```

#### Error Response (404 Not Found):
```json
{
  "error": "Appointment not found or you don't have permission to view it"
}
```

#### Error Response (401 Unauthorized):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 📊 Response Fields Explanation

### Appointment Fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique appointment ID |
| `doctor_details` | object | Complete doctor information (see below) |
| `slot` | integer | TimeSlot ID |
| `slot_details` | object | Time slot information (start/end times) |
| `patient_name` | string | Name of the patient |
| `patient_phone` | string | Phone number of the patient |
| `patient_email` | string | Email of the patient |
| `patient_age` | integer | Age of the patient |
| `patient_gender` | string | Gender of the patient |
| `patient_mrn` | string | Medical Record Number |
| `patient_weight` | string | Weight of the patient (e.g., "65kg") |
| `patient_disease` | string | Primary disease/condition |
| `patient_heart_rate` | string | Heart rate (e.g., "75 bpm") |
| `patient_blood_type` | string | Blood type (e.g., "O+") |
| `patient_photo` | file URL | Photo of the patient (if available) |
| `appointment_type` | string | Type of appointment (e.g., "Follow-up Consultation") |
| `location` | string | Location where appointment will be held (e.g., "Room 501") |
| `start_time` | datetime | Appointment start time (ISO 8601 format) |
| `end_time` | datetime | Appointment end time (ISO 8601 format) |
| `status` | string | Current status (pending, confirmed, booked, cancelled, rejected, outpatient) |
| `reschedule_reason` | string | Reason for rescheduling (if applicable) |
| `rejection_reason` | string | Reason for rejection (if applicable) |
| `created_at` | datetime | When the appointment was created |

### Doctor Details Fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Doctor's unique ID |
| `first_name` | string | Doctor's first name |
| `last_name` | string | Doctor's last name |
| `full_name` | string | Doctor's full name (concatenated) |
| `mobile_number` | string | Doctor's mobile number |
| `alternate_number` | string | Doctor's alternate phone number |
| `email` | string | Doctor's email address |
| `city` | string | City where doctor practices |
| `address` | string | Doctor's full address |
| `gender` | string | Gender (male/female/other) |

---

## 🔧 Frontend Integration Examples

### JavaScript/React Example:
```javascript
// Get all appointments
const getPatientAppointments = async (token) => {
  try {
    const response = await fetch('/api/appointments/patient/appointments/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    if (response.ok) {
      console.log('Appointments:', data.appointments);
      return data.appointments;
    } else {
      console.error('Error:', data);
    }
  } catch (error) {
    console.error('API Error:', error);
  }
};

// Get specific appointment
const getAppointmentDetail = async (appointmentId, token) => {
  try {
    const response = await fetch(`/api/appointments/patient/appointments/${appointmentId}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    if (response.ok) {
      console.log('Appointment Detail:', data.appointment);
      return data.appointment;
    } else {
      console.error('Error:', data);
    }
  } catch (error) {
    console.error('API Error:', error);
  }
};

// Filter by status
const getConfirmedAppointments = async (token) => {
  try {
    const response = await fetch('/api/appointments/patient/appointments/?status=confirmed', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    if (response.ok) {
      return data.appointments;
    }
  } catch (error) {
    console.error('API Error:', error);
  }
};
```

### Python Example:
```python
import requests

# Get all appointments
def get_patient_appointments(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        'http://localhost:8000/api/appointments/patient/appointments/',
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total Appointments: {data['count']}")
        for appt in data['appointments']:
            print(f"Doctor: {appt['doctor_details']['full_name']}")
            print(f"Date: {appt['start_time']}")
            print(f"Status: {appt['status']}\n")
    else:
        print(f"Error: {response.json()}")

# Get specific appointment
def get_appointment_detail(appointment_id, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f'http://localhost:8000/api/appointments/patient/appointments/{appointment_id}/',
        headers=headers
    )
    
    if response.status_code == 200:
        appt = response.json()['appointment']
        print(f"Doctor: {appt['doctor_details']['full_name']}")
        print(f"Email: {appt['doctor_details']['email']}")
        print(f"Phone: {appt['doctor_details']['mobile_number']}")
        print(f"Location: {appt['location']}")
        print(f"Time: {appt['start_time']} to {appt['end_time']}")
    else:
        print(f"Error: {response.json()}")
```

---

## ✅ Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters or date format |
| 401 | Unauthorized | Missing or invalid authentication token |
| 404 | Not Found | Appointment not found or no permission to view |
| 500 | Server Error | Internal server error |

---

## 🔒 Security Notes

1. **Authentication Required**: All patient endpoints require valid JWT token
2. **Data Privacy**: Patients can only view their own appointments (filtered by user ID or email)
3. **Read-Only**: Patient endpoints are read-only (no modifications allowed)
4. **Token Expiration**: JWT tokens expire after 30 minutes; refresh token to get new access token

---

## 🚀 Usage Summary

```
1. Authenticate user at /auth/login/ to get JWT token
2. Use GET /patient/appointments/ to list all appointments
3. Optionally filter by status or date range
4. Use GET /patient/appointments/<id>/ for detailed view of a specific appointment
5. Appointments include complete doctor details for reference
```

---

## 📝 Example Use Cases

### Patient Dashboard:
Display all upcoming confirmed appointments with doctor details

### Patient Notifications:
Show pending appointment requests requiring patient confirmation

### Appointment Reminders:
Filter appointments by date and send reminders to patients

### Medical History:
Display past appointments and doctor information for patient records

---

## 🐛 Troubleshooting

### "Authentication credentials were not provided"
- Ensure JWT token is included in Authorization header
- Check token format: `Bearer <token>`
- Verify token hasn't expired

### "Appointment not found"
- Verify the appointment ID is correct
- Ensure the appointment belongs to the authenticated user
- Check if appointment was cancelled/deleted

### "Invalid date format"
- Use YYYY-MM-DD format for date parameters
- Example: 2025-01-15

---

## 📞 Support
For issues or questions, contact the development team or check the main API documentation.
