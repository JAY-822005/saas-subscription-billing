import pytest

from apps.subscriptions.models import Subscription
from tests.factories import (
    OrganizationFactory,
    SubscriptionPlanFactory,
)


@pytest.mark.django_db
def test_create_subscription():
    organization = OrganizationFactory()
    plan = SubscriptionPlanFactory()

    subscription = Subscription.objects.create(
        organization=organization,
        plan=plan,
        billing_cycle="monthly",
        status="trial",
    )

    assert subscription.organization == organization
    assert subscription.plan == plan
    assert subscription.status == "trial"