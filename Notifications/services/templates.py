def appointment_template(user_name, date):
    return {
        "title": "Appointment Reminder",
        "body": f"Hi {user_name}, your appointment is on {date}"
    }
