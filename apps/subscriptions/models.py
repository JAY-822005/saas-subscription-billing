from django.db import models

from apps.core.models import BaseModel
from apps.organizations.models import Organization


class SubscriptionPlan(BaseModel):
    BILLING_CYCLE_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    yearly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    max_users = models.PositiveIntegerField(
        default=5
    )

    usage_limit = models.PositiveIntegerField(
        default=1000
    )

    free_trial_days = models.PositiveIntegerField(
        default=14
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    STATUS_CHOICES = (
        ("trial", "Trial"),
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
        ("past_due", "Past Due"),
    )

    BILLING_CYCLE_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="trial"
    )

    billing_cycle = models.CharField(
        max_length=20,
        choices=BILLING_CYCLE_CHOICES,
        default="monthly"
    )

    trial_ends_at = models.DateTimeField(
        null=True,
        blank=True
    )

    starts_at = models.DateTimeField(
        auto_now_add=True
    )

    renews_at = models.DateTimeField(
        null=True,
        blank=True
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    auto_renew = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.organization.name} - {self.plan.name}"