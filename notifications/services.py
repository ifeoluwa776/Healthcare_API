from django.core.mail import send_mail
from django.conf import settings


def send_notification_email(notification):
    user = notification.user

    if not user.email:
        return

    send_mail(
        subject=notification.title,
        message=notification.message,
        from_email=getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            "noreply@healthcareapi.com",
        ),
        recipient_list=[user.email],
        fail_silently=False,
    )

