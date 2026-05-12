# reminders/views.py
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Reminder
from .serializers import ReminderSerializer

TIME_MAP = {
    "morning": "08:00",
    "afternoon": "13:00",
    "evening": "18:00",
    "night": "21:00"
}

@api_view(['GET'])
def list_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)
    serializer = ReminderSerializer(reminders, many=True)
    return Response(serializer.data)

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
def update_reminder(request, id):
    try:
        reminder = Reminder.objects.get(id=id)
    except Reminder.DoesNotExist:
        return Response({"error": "Reminder not found"}, status=404)

    data = request.data
    if "medicine_name" in data:
        reminder.medicine_name = data["medicine_name"]
    if "dosage" in data:
        reminder.dosage = data["dosage"]
    if "frequency" in data:
        reminder.frequency = data["frequency"]
    
    # Handle duration update (recalculate end_date)
    if "duration_days" in data:
        try:
            duration = int(data["duration_days"])
            reminder.duration_days = duration
            reminder.end_date = reminder.start_date + timedelta(days=duration)
        except ValueError:
            pass

    # Handle times update (recalculate next_trigger)
    if "times" in data and isinstance(data["times"], list) and len(data["times"]) > 0:
        reminder.times = data["times"]
        first_time = TIME_MAP.get(data["times"][0].lower(), "08:00")
        try:
            new_trigger_time = datetime.strptime(first_time, "%H:%M").time()
            reminder.next_trigger = datetime.combine(datetime.today().date(), new_trigger_time)
            # If time has already passed today, set for tomorrow
            if reminder.next_trigger < datetime.now():
                reminder.next_trigger += timedelta(days=1)
        except Exception:
            pass

    reminder.save()
    return Response({"message": "Reminder updated successfully"})


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
