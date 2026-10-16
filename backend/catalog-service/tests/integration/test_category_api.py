import pytest


@pytest.fixture(autouse=True)
def clear_categories(test_client):
    response = test_client.get("/api/v1/public/categories/")
    assert response.status_code == 200

    for category in response.json()["result"]:
        delete_response = test_client.delete(
            f"/api/v1/admin/categories/{category['id']}",
        )
        assert delete_response.status_code == 204


class TestCreateCategory:
    def test_success(self, test_client):
        name = " Category1"
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        )
        resp_data = resp.json()

        assert resp.status_code == 201
        assert resp_data["id"]
        assert resp_data["name"] == name.strip()

    def test_rejects_duplicate(self, test_client, category1):
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": category1["name"]},
        )

        assert resp.status_code == 409
        assert "already exists" in resp.json()["error"]

    @pytest.mark.parametrize("name", ["", "   ", "\t", "\n", " \t\n "])
    def test_rejects_empty_or_whitespace_name(self, test_client, name):
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        )

        assert resp.status_code == 400
        assert resp.json()["error"] == "Category name cannot be empty."

    def test_rejects_name_shorter_than_two_characters(self, test_client):
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": "a"},
        )

        assert resp.status_code == 400
        assert "at least 2 characters" in resp.json()["error"]

    def test_rejects_name_longer_than_32_characters(self, test_client):
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": "x" * 33},
        )

        assert resp.status_code == 400
        assert "at most 32 characters" in resp.json()["error"]

    @pytest.mark.parametrize("name", ["a1", "x" * 32])
    def test_accepts_name_length_boundaries(self, test_client, name):
        resp = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        )

        assert resp.status_code == 201
        assert resp.json()["name"] == name


class TestCategoryQueries:
    def test_get_category(self, test_client, category1):
        response = test_client.get(
            f"/api/v1/public/categories/{category1['id']}",
        )

        assert response.status_code == 200
        assert response.json() == category1

    def test_get_category_returns_not_found(self, test_client):
        response = test_client.get(
            "/api/v1/public/categories/00000000-0000-0000-0000-000000000000",
        )

        assert response.status_code == 404
        assert "was not found" in response.json()["error"]

    def test_get_all_categories(self, test_client):
        name = "test-category"
        created = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        ).json()

        response = test_client.get("/api/v1/public/categories/")

        assert response.status_code == 200
        assert created in response.json()["result"]


class TestUpdateCategory:
    def test_success(self, test_client, category1):
        name = "updated-category"
        response = test_client.patch(
            f"/api/v1/admin/categories/{category1['id']}",
            json={"name": name},
        )

        assert response.status_code == 201
        assert response.json() == {"id": category1["id"], "name": name}

    def test_rejects_nonexistent_category(self, test_client):
        response = test_client.patch(
            "/api/v1/admin/categories/00000000-0000-0000-0000-000000000000",
            json={"name": "updated-category"},
        )

        assert response.status_code == 404
        assert "was not found" in response.json()["error"]

    @pytest.mark.parametrize(
        ("name", "error"),
        [
            ("", "Category name cannot be empty."),
            ("a", "at least 2 characters"),
            ("x" * 33, "at most 32 characters"),
        ],
    )
    def test_rejects_invalid_name(self, test_client, category1, name, error):
        response = test_client.patch(
            f"/api/v1/admin/categories/{category1['id']}",
            json={"name": name},
        )

        assert response.status_code == 400
        assert error in response.json()["error"]

    def test_rejects_duplicate_name(self, test_client, category1):
        duplicate = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": "another-category"},
        ).json()

        response = test_client.patch(
            f"/api/v1/admin/categories/{category1['id']}",
            json={"name": duplicate["name"]},
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["error"]

    def test_rejects_unchanged_name(self, test_client, category1):
        response = test_client.patch(
            f"/api/v1/admin/categories/{category1['id']}",
            json={"name": category1["name"]},
        )

        assert response.status_code == 400
        assert "equivalent new name" in response.json()["error"]


class TestDeleteCategory:
    def test_success(self, test_client):
        name = "test-category"
        created = test_client.post(
            "/api/v1/admin/categories/",
            json={"name": name},
        ).json()

        response = test_client.delete(
            f"/api/v1/admin/categories/{created['id']}",
        )

        assert response.status_code == 204
        assert test_client.get(
            f"/api/v1/public/categories/{created['id']}",
        ).status_code == 404

    def test_rejects_nonexistent_category(self, test_client):
        response = test_client.delete(
            "/api/v1/admin/categories/00000000-0000-0000-0000-000000000000",
        )

        assert response.status_code == 404
        assert "was not found" in response.json()["error"]