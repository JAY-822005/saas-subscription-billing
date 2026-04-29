from apps.subscriptions.models import Subscription
from apps.invoices.models import Invoice
from apps.billing.models import PaymentRecovery
from apps.usage_tracking.models import UsageRecord


def get_dashboard_metrics(user):
    subscriptions = Subscription.objects.filter(
        organization__owner=user
    )

    invoices = Invoice.objects.filter(
        organization__owner=user
    )

    payment_failures = PaymentRecovery.objects.filter(
        organization__owner=user
    )

    usage_records = UsageRecord.objects.filter(
        organization__owner=user,
        is_over_limit=True
    )

    monthly_revenue = sum(
        invoice.amount
        for invoice in invoices.filter(status="paid")
    )

    return {
        "total_subscriptions": subscriptions.count(),
        "active_subscriptions": subscriptions.filter(
            status="active"
        ).count(),
        "trial_subscriptions": subscriptions.filter(
            status="trial"
        ).count(),
        "cancelled_subscriptions": subscriptions.filter(
            status="cancelled"
        ).count(),

        "paid_invoices": invoices.filter(
            status="paid"
        ).count(),

        "pending_invoices": invoices.filter(
            status="pending"
        ).count(),

        "failed_payments": payment_failures.filter(
            status="failed"
        ).count(),

        "upgrade_recommendations": usage_records.count(),

        "monthly_revenue": monthly_revenue,
    }