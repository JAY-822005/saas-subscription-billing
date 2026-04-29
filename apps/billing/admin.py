from django.contrib import admin
from .models import PaymentRecovery


@admin.register(PaymentRecovery)
class PaymentRecoveryAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "invoice",
        "status",
        "retry_count",
        "max_retries",
        "next_retry_at",
    )

    list_filter = (
        "status",
        "retry_count",
    )

    search_fields = (
        "organization__name",
        "invoice__invoice_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "recovered_at",
    )