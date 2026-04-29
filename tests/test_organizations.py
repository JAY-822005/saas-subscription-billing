import pytest

from tests.factories import (
    UserFactory,
    OrganizationFactory,
)


@pytest.mark.django_db
def test_create_organization():
    user = UserFactory()

    organization = OrganizationFactory(
        owner=user
    )

    assert organization.owner == user
    assert organization.name is not None