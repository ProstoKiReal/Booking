import pytest


class TestCreateCategory:
    def test_success(self, test_client):
        name = " Category1"
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        )
        resp_data = resp .json()

        assert resp .status_code == 200
        assert resp_data["id"]
        assert resp_data["name"] == name.strip()

    def test_rejects_duplicate(self, test_client, category1):
        resp= test_client.post(
            "/api/v1/admin/categories/",
            json={"name": category1["name"]},
        )

        assert resp.status_code == 409
        assert "already exists" in resp.json()["error"]

    @pytest.mark.parametrize("name", ["", "   ", "\t", "\n", " \t\n "])
    def test_rejects_empty_or_whitespace_name(self, test_client, name):
        resp= test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        )

        assert resp.status_code == 400
        assert resp.json()["error"] == "Category name cannot be empty."

    def test_rejects_name_shorter_than_two_characters(self, test_client):
        resp= test_client.post(
            "/api/v1/admin/categories/",
            json={"name": "a"},
        )

        assert resp.status_code == 400
        assert "at least 2 characters" in resp.json()["error"]

    def test_rejects_name_longer_than_32_characters(self, test_client):
        resp= test_client.post(
            "/api/v1/admin/categories/",
            json={"name": "x" * 33},
        )

        assert resp.status_code == 400
        assert "at most 32 characters" in resp.json()["error"]

    @pytest.mark.parametrize("name", ["a1", "x" * 32])
    def test_accepts_name_length_boundaries(self, test_client, name):
        resp= test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        )

        assert resp.status_code == 200
        assert resp.json()["name"] == name
