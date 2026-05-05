from celery import shared_task
from django.utils import timezone
from .models import Reminder, FCMToken
from .fcm import send_fcm_notification

@shared_task
def dispatch_due_reminders():
    now = timezone.now()
    due_reminders = Reminder.objects.filter(
        is_active=True,
        next_reminder_datetime__lte=now,
        snooze_until__isnull=True   # not snoozed
    ) | Reminder.objects.filter(
        is_active=True,
        next_reminder_datetime__lte=now,
        snooze_until__lte=now       # snoozed but snooze_until has passed
    )

    # To ensure distinct if there's overlap in complex queries
    due_reminders = due_reminders.distinct()

    for reminder in due_reminders:
        # 1. Send push notification (FCM)
        user_tokens = FCMToken.objects.filter(user=reminder.user).values_list('token', flat=True)
        for token in user_tokens:
            send_fcm_notification(token, f"Time to take {reminder.medicine}", body="Please take your prescribed medicine.")

        # 2. Compute next occurrence based on frequency
        reminder.next_reminder_datetime = reminder.compute_next_datetime()
        # Reset snooze
        reminder.snooze_until = None
        
        # If no next date, mark inactive
        if not reminder.next_reminder_datetime:
            reminder.is_active = False
            
        reminder.save(update_fields=['next_reminder_datetime', 'snooze_until', 'is_active'])

    return f"Dispatched {due_reminders.count()} reminders."
