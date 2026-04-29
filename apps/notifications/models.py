from django.db import models

from apps.core.models import BaseModel
from apps.organizations.models import Organization


class Notification(BaseModel):
    TYPE_CHOICES = (
        ("trial_reminder", "Trial Reminder"),
        ("renewal_reminder", "Renewal Reminder"),
        ("payment_failed", "Payment Failed"),
        ("invoice_due", "Invoice Due"),
        ("upgrade_suggestion", "Upgrade Suggestion"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )

    scheduled_for = models.DateTimeField()

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title