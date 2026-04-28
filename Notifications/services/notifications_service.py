from .models import Device
from .services.fcm import send_push_notification
from .services.email_service import send_email
from .services.sms_service import send_sms
from .services.templates import appointment_template

def send_notification(user, email, phone):
    data = appointment_template(user.username, "Tomorrow")

    # Push
    devices = Device.objects.filter(user=user)
    for device in devices:
        send_push_notification(device.fcm_token, data["title"], data["body"])

    # Email
    send_email(data["title"], email, {"message": data["body"]})

    # SMS
    send_sms(phone, data["body"])
