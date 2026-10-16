import pytest
import httpx


@pytest.fixture
def test_client():
    with httpx.Client(base_url="http://catalog-test-app:8000") as client:
        yield client
