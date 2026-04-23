# reminders/views.py
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Reminder

TIME_MAP = {
    "morning": "08:00",
    "afternoon": "13:00",
    "evening": "18:00",
    "night": "21:00"
}

@api_view(['POST'])
def create_reminder(request):
    data = request.data

    start_date = datetime.today().date()
    duration = int(data["duration_days"])
    end_date = start_date + timedelta(days=duration)

    first_time = TIME_MAP[data["times"][0]]

    next_trigger = datetime.strptime(
        f"{start_date} {first_time}",
        "%Y-%m-%d %H:%M"
    )

    Reminder.objects.create(
        user=request.user,
        medicine_name=data["medicine_name"],
        dosage=data["dosage"],
        frequency=data["frequency"],
        duration_days=duration,
        times=data["times"],
        start_date=start_date,
        end_date=end_date,
        next_trigger=next_trigger
    )

    return Response({"message": "Reminder created"})


@api_view(['PATCH'])
def snooze_reminder(request, id):
    reminder = Reminder.objects.get(id=id)

    minutes = int(request.data.get("minutes", 10))
    reminder.next_trigger += timedelta(minutes=minutes)
    reminder.status = "snoozed"
    reminder.save()

    return Response({"message": "Snoozed"})


@api_view(['PATCH'])
def dismiss_reminder(request, id):
    reminder = Reminder.objects.get(id=id)

    reminder.status = "done"
    reminder.save()

    return Response({"message": "Dismissed"})
