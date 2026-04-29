from celery import shared_task
from django.utils import timezone

from .models import Notification


@shared_task
def send_scheduled_notification(notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id
        )

        if notification.status == "sent":
            return "Notification already sent"

        # Simulated email sending
        # Replace later with SendGrid / SMTP / AWS SES

        email_sent_successfully = True

        if email_sent_successfully:
            notification.status = "sent"
            notification.sent_at = timezone.now()
            notification.save()

            return "Notification sent successfully"

        notification.status = "failed"
        notification.save()

        return "Notification failed"

    except Notification.DoesNotExist:
        return "Notification not found"