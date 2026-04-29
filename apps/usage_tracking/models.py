from django.db import models

from apps.core.models import BaseModel
from apps.organizations.models import Organization
from apps.subscriptions.models import SubscriptionPlan


class UsageRecord(BaseModel):
    FEATURE_CHOICES = (
        ("api_calls", "API Calls"),
        ("team_members", "Team Members"),
        ("reports_generated", "Reports Generated"),
        ("storage_usage", "Storage Usage"),
        ("emails_sent", "Emails Sent"),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="usage_records"
    )

    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="usage_records"
    )

    feature_name = models.CharField(
        max_length=100,
        choices=FEATURE_CHOICES
    )

    used_units = models.PositiveIntegerField(
        default=0
    )

    usage_limit = models.PositiveIntegerField(
        default=1000
    )

    is_over_limit = models.BooleanField(
        default=False
    )

    billing_month = models.DateField()

    def save(self, *args, **kwargs):
        self.is_over_limit = self.used_units > self.usage_limit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organization.name} - {self.feature_name}"