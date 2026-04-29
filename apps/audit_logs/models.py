from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import BaseModel
from apps.organizations.models import Organization

User = get_user_model()


class AuditLog(BaseModel):

    ACTION_TYPES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("payment", "Payment"),
        ("subscription_change", "Subscription Change"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_TYPES
    )

    model_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    object_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.action} by {self.user}"