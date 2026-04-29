import pytest
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.mark.django_db
def test_jwt_token_obtain():
    password = "testpass123"

    user = UserFactory()
    user.set_password(password)
    user.save()

    client = APIClient()

    response = client.post(
        "/api/token/",
        {
            "email": user.email,
            "password": password,
        },
        format="json"
    )

    print("DEBUG RESPONSE:", response.data)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data