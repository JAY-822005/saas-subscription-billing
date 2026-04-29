from django.contrib import admin
from .models import UsageRecord


@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "feature_name",
        "used_units",
        "usage_limit",
        "is_over_limit",
        "billing_month",
    )

    list_filter = (
        "feature_name",
        "is_over_limit",
        "billing_month",
    )

    search_fields = (
        "organization__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )