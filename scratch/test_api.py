import requests
import json

url = "http://127.0.0.1:8000/api/doctor-slots/"
data = {
    "from_date": "2026-05-12",
    "to_date": "2026-05-13",
    "from_time": "10:00:00",
    "to_time": "12:00:00",
    "slot_duration": 30,
    "doctor": 1  # Assuming doctor ID 1 exists
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
