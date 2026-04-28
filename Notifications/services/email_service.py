from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_email(subject, to_email, context):
    html_content = render_to_string("email/appointment.html", context)

    send_mail(
        subject,
        "",
        "noreply@vaidyago.com",
        [to_email],
        html_message=html_content
    )
