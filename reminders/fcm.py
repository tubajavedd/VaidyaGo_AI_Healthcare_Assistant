import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os

# Only initialize once
if not firebase_admin._apps:
    try:
        # Provide fallback if FIREBASE_CREDENTIALS is not fully set up
        if hasattr(settings, 'FIREBASE_CREDENTIALS') and os.path.exists(settings.FIREBASE_CREDENTIALS):
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred)
        else:
            print("Warning: FIREBASE_CREDENTIALS path is missing or invalid. FCM will not work.")
    except Exception as e:
        print(f"Error initializing Firebase Admin: {e}")

def send_fcm_notification(device_token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=device_token,
        )
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending FCM message: {e}")
        return None
