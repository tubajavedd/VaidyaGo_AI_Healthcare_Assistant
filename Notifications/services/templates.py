def otp_email_template(otp):
    return {
        "title": "Your OTP",
        "body": f"Your OTP is {otp}. It expires in 5 minutes."
    }


def appointment_email_template(user_name, date):
    return {
        "title": "Appointment Reminder",
        "body": f"Hello {user_name}, your appointment is scheduled on {date}"
    }
