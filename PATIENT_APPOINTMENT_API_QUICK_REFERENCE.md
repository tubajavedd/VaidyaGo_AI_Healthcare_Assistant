# 👤 Patient Appointment API - Quick Reference

## Overview
Two new patient-focused endpoints have been added to allow patients to view their appointments with complete doctor information.

## 🔗 New Endpoints

### 1. List Patient's Appointments
```
GET /api/appointments/patient/appointments/
```

**Purpose**: Get all appointments for the authenticated patient

**Required**: JWT Authentication Token

**Query Parameters** (optional):
- `status` - Filter by status (pending, confirmed, booked, cancelled, rejected, outpatient)
- `date_from` - Filter from date (YYYY-MM-DD format)
- `date_to` - Filter until date (YYYY-MM-DD format)

**Response Includes**:
- Full doctor details (name, contact, location, address)
- Appointment details (date, time, type, location)
- Patient clinical information
- Appointment status

**Example**:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/?status=confirmed" \
  -H "Authorization: Bearer <token>"
```

---

### 2. Get Appointment Details
```
GET /api/appointments/patient/appointments/<appointment_id>/
```

**Purpose**: Get detailed information about a specific appointment

**Required**: JWT Authentication Token

**Path Parameters**:
- `appointment_id` - The ID of the appointment

**Response Includes**:
- Complete doctor information
- Full appointment details
- Time slot information
- Patient medical records

**Example**:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/1/" \
  -H "Authorization: Bearer <token>"
```

---

## 📊 Response Structure

### Sample Response for List Endpoint:
```json
{
  "message": "Appointments retrieved successfully",
  "count": 2,
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
      "patient_name": "Jane Smith",
      "appointment_type": "Follow-up Consultation",
      "location": "Room 501",
      "start_time": "2025-01-20T10:00:00Z",
      "end_time": "2025-01-20T10:30:00Z",
      "status": "confirmed",
      "created_at": "2025-01-15T14:30:00Z"
    }
  ]
}
```

---

## 🔐 Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer your_jwt_token_here
```

To get a token:
1. Sign up or login at `/auth/signup/` or `/auth/login/`
2. Use the returned JWT token for subsequent requests

---

## 🧪 Testing with cURL

### Get all appointments:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Get appointments with status filter:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/?status=confirmed" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Get appointments in date range:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/?date_from=2025-01-01&date_to=2025-12-31" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Get specific appointment:
```bash
curl -X GET "http://localhost:8000/api/appointments/patient/appointments/1/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 🛡️ Security Features

✅ **Authentication Required** - All endpoints require valid JWT token
✅ **Data Privacy** - Patients can only view their own appointments
✅ **Read-Only** - No modification allowed through patient endpoints
✅ **User Filtering** - Appointments filtered by authenticated user ID or email

---

## ✅ Implementation Details

### Files Modified:
1. **appointments/serializers.py** - Added `DoctorDetailSerializer` and `PatientAppointmentSerializer`
2. **appointments/views.py** - Added `patient_appointments()` and `patient_appointment_detail()` views
3. **appointments/urls.py** - Added new patient endpoints

### Key Features:
- Automatic filtering by authenticated user
- Support for status filtering (pending, confirmed, booked, cancelled, rejected, outpatient)
- Date range filtering (from/to)
- Includes complete doctor contact information
- Includes appointment details and clinical information
- Sorted by latest appointment first

---

## 📋 Doctor Information Included

The `doctor_details` object includes:
- Full name (first_name + last_name)
- Contact number (mobile_number, alternate_number)
- Email address
- Location (city, full address)
- Gender

---

## 🚀 Frontend Integration

### React Example:
```jsx
const PatientAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const token = localStorage.getItem('jwt_token');

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    const response = await fetch('/api/appointments/patient/appointments/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    setAppointments(data.appointments);
  };

  return (
    <div>
      {appointments.map(appt => (
        <div key={appt.id}>
          <h3>Dr. {appt.doctor_details.full_name}</h3>
          <p>Date: {new Date(appt.start_time).toLocaleDateString()}</p>
          <p>Time: {new Date(appt.start_time).toLocaleTimeString()}</p>
          <p>Location: {appt.location}</p>
          <p>Status: {appt.status}</p>
          <p>Contact: {appt.doctor_details.mobile_number}</p>
        </div>
      ))}
    </div>
  );
};
```

---

## 📞 Status Codes

| Code | Message | Solution |
|------|---------|----------|
| 200 | OK | ✅ Request successful |
| 400 | Bad Request | ❌ Check date format (YYYY-MM-DD) |
| 401 | Unauthorized | ❌ Add valid JWT token to header |
| 404 | Not Found | ❌ Check appointment ID or permissions |

---

## 🎯 Use Cases

1. **Patient Dashboard** - Display all upcoming appointments
2. **Appointment Details** - Show doctor contact and appointment location
3. **Filter View** - Show only confirmed appointments
4. **Reminders** - Get appointments for today/tomorrow
5. **Medical History** - View past appointments and doctors

---

## 📝 Notes

- Appointments are sorted by latest first (descending by date)
- Empty result returns `{"count": 0, "appointments": []}`
- All timestamps are in ISO 8601 format (UTC)
- Patients are identified by `user.id` or `patient_email`

---

For full documentation, see **PATIENT_APPOINTMENT_API.md**
