from rest_framework import serializers

from .models import PaymentRecovery


class PaymentRecoverySerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    invoice_number = serializers.ReadOnlyField(
        source="invoice.invoice_number"
    )

    class Meta:
        model = PaymentRecovery
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "retry_count",
            "next_retry_at",
            "recovered_at",
        ]