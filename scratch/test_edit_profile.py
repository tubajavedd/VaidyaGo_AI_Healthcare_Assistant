import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaidyaGo.settings")
django.setup()

from chatbot.services.tool_router import ToolRouter
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first() # Get any user for testing

if user:
    print(f"Testing Edit_profile for user: {user.username}")
    
    # Test data
    intent_data = {
        "action": "Edit_profile",
        "data": {
            "full_name": "Test User Updated",
            "phone_number": "9876543210",
            "residential_address": "123 Test Street, City"
        }
    }
    
    response = ToolRouter.execute(intent_data, user)
    print("Response:", response)
    
    # Verify in DB
    from editProfile.models import editProfile
    profile = editProfile.objects.get(user=user)
    print(f"Profile Full Name: {profile.full_name}")
    print(f"Profile Phone: {profile.phone_number}")
    print(f"Profile Address: {profile.residential_address}")
else:
    print("No user found in DB to test.")
