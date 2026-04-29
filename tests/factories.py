import factory
from django.contrib.auth import get_user_model

from apps.organizations.models import Organization
from apps.subscriptions.models import SubscriptionPlan


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(
        lambda n: f"user{n}"
    )

    email = factory.Sequence(
        lambda n: f"user{n}@example.com"
    )

    role = "owner"
    
    password = factory.PostGenerationMethodCall(
        "set_password",
        "testpass123"
    )


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(
        lambda n: f"Organization {n}"
    )

    owner = factory.SubFactory(UserFactory)


class SubscriptionPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubscriptionPlan

    name = factory.Sequence(
        lambda n: f"Plan {n}"
    )

    monthly_price = 99
    yearly_price = 999
    max_users = 10
    usage_limit = 1000