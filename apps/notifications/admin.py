from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "notification_type",
        "status",
        "scheduled_for",
        "sent_at",
    )

    list_filter = (
        "notification_type",
        "status",
    )

    search_fields = (
        "title",
        "organization__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "sent_at",
    )