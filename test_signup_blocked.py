import os
import sys
import django
import json
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from django.test import Client

def test_admin_signup_blocked():
    client = Client()
    data = {
        "usertype": "admin",
        "email": "testadmin@example.com",
        "phone": "+919876543210",
        "password": "testpassword",
        "confirm_password": "testpassword"
    }
    response = client.post('/accounts/api/signup/', data=json.dumps(data), content_type='application/json')
    print(f"Signup Result: {response.status_code}")
    print(f"Response: {response.content.decode()}")
    
    if response.status_code == 403:
        print("PASS: Admin signup is blocked.")
    else:
        print("FAIL: Admin signup is NOT blocked.")

if __name__ == '__main__':
    test_admin_signup_blocked()
