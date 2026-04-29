from celery import shared_task
from django.utils import timezone

from .models import PaymentRecovery
from .services import calculate_next_retry


@shared_task
def process_payment_recovery(payment_recovery_id):
    try:
        recovery = PaymentRecovery.objects.get(
            id=payment_recovery_id
        )

        if recovery.status in ["recovered", "failed"]:
            return "Recovery already completed"

        if recovery.retry_count >= recovery.max_retries:
            recovery.status = "failed"
            recovery.save()
            return "Max retries exceeded"

        recovery.retry_count += 1
        recovery.status = "retrying"
        recovery.next_retry_at = calculate_next_retry(
            recovery.retry_count
        )

        # Simulated payment gateway retry
        # Replace with Stripe/Razorpay logic later

        payment_successful = False

        if payment_successful:
            recovery.status = "recovered"
            recovery.recovered_at = timezone.now()

            recovery.invoice.status = "paid"
            recovery.invoice.save()

        recovery.save()

        return f"Retry attempt {recovery.retry_count} processed"

    except PaymentRecovery.DoesNotExist:
        return "Payment recovery not found"