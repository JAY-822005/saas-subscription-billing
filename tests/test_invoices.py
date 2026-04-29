import pytest
from datetime import date

from apps.invoices.models import Invoice
from apps.subscriptions.models import Subscription
from tests.factories import (
    OrganizationFactory,
    SubscriptionPlanFactory,
)


@pytest.mark.django_db
def test_create_invoice():
    organization = OrganizationFactory()
    plan = SubscriptionPlanFactory()

    subscription = Subscription.objects.create(
        organization=organization,
        plan=plan,
        billing_cycle="monthly",
        status="active",
    )

    invoice = Invoice.objects.create(
        organization=organization,
        subscription=subscription,
        invoice_number="INV-TEST-001",
        amount=199.99,
        due_date=date.today(),
        status="pending",
    )

    assert invoice.organization == organization
    assert invoice.subscription == subscription
    assert invoice.status == "pending"