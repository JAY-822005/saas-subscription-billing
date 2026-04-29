from rest_framework import serializers

from .models import Invoice
from .services import generate_invoice_number


class InvoiceSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "invoice_number",
            "issued_at",
            "paid_at",
        ]

    def create(self, validated_data):
        validated_data["invoice_number"] = generate_invoice_number()
        return super().create(validated_data)