# reminders/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Reminder
from .utils import send_push_notification, update_next_trigger

@shared_task
def check_reminders():
    now = timezone.now()

    reminders = Reminder.objects.filter(
        next_trigger__lte=now,
        status="pending"
    )

    for reminder in reminders:
        send_push_notification(reminder)
        update_next_trigger(reminder)
