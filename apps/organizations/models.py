from django.db import models
from apps.users.models import User


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    slug = models.SlugField(
        unique=True,
        help_text="Unique organization identifier"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_organizations"
    )

    contact_email = models.EmailField()

    is_active = models.BooleanField(default=True)

    trial_ends_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name