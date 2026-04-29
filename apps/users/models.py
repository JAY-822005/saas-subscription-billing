from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("super_admin", "Super Admin"),
        ("org_admin", "Organization Admin"),
        ("manager", "Manager"),
        ("member", "Member"),
        ("billing_admin", "Billing Admin"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="member"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_email_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"    
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email