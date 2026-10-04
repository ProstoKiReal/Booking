import pytest


@pytest.fixture
def category1(test_client):
    name = f"category1"
    response = test_client.post(
        "/api/v1/admin/categories/",
        json={"name": name},
    )
    return response.json()