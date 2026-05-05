# reminders/utils.py
from datetime import timedelta
import requests

TIME_MAP = {
    "morning": 8,
    "afternoon": 13,
    "evening": 18,
    "night": 21
}

def update_next_trigger(reminder):
    times = reminder.times
    current_hour = reminder.next_trigger.hour

    next_time = None

    for t in times:
        if TIME_MAP[t] > current_hour:
            next_time = TIME_MAP[t]
            break

    if next_time:
        reminder.next_trigger = reminder.next_trigger.replace(hour=next_time)
    else:
        next_day = reminder.next_trigger + timedelta(days=1)
        first_time = TIME_MAP[times[0]]
        reminder.next_trigger = next_day.replace(hour=first_time)

    if reminder.next_trigger.date() > reminder.end_date:
        reminder.status = "done"

    reminder.save()


def send_push_notification(reminder):
    fcm_token = reminder.user.profile.fcm_token

    payload = {
        "to": fcm_token,
        "notification": {
            "title": "Medicine Reminder 💊",
            "body": f"Take {reminder.medicine_name} ({reminder.dosage})"
        }
    }

    headers = {
        "Authorization": "key=YOUR_FCM_SERVER_KEY",
        "Content-Type": "application/json"
    }

    requests.post(
        "https://fcm.googleapis.com/fcm/send",
        json=payload,
        headers=headers
    )
