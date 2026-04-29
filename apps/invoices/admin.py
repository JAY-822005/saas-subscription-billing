from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "organization",
        "amount",
        "status",
        "due_date",
        "issued_at",
    )

    list_filter = (
        "status",
        "due_date",
        "issued_at",
    )

    search_fields = (
        "invoice_number",
        "organization__name",
    )

    readonly_fields = (
        "invoice_number",
        "issued_at",
        "created_at",
        "updated_at",
    )