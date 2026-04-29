from django.db import models

from apps.core.models import BaseModel
from apps.organizations.models import Organization
from apps.invoices.models import Invoice


class PaymentRecovery(BaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("retrying", "Retrying"),
        ("recovered", "Recovered"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="payment_recoveries"
    )

    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payment_recovery"
    )

    retry_count = models.PositiveIntegerField(
        default=0
    )

    max_retries = models.PositiveIntegerField(
        default=3
    )

    next_retry_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )

    failure_reason = models.TextField(
        blank=True,
        null=True
    )

    recovered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.organization.name} - {self.invoice.invoice_number}"