from django.contrib import admin

from .models import SubscriptionPlan, Subscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "monthly_price",
        "yearly_price",
        "max_users",
        "usage_limit",
        "is_active",
    )

    list_filter = (
        "is_active",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "plan",
        "status",
        "billing_cycle",
        "renews_at",
        "auto_renew",
    )

    list_filter = (
        "status",
        "billing_cycle",
        "auto_renew",
    )