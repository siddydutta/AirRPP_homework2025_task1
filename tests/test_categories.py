import pytest
from fastapi.testclient import TestClient


def test_create_category(client: TestClient):
    category_data = {
        "title": "Test Category",
        "description": "A test category"
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == category_data["title"]
    assert data["description"] == category_data["description"]
    assert "id" in data


def test_create_category_without_description(client: TestClient):
    category_data = {
        "title": "Test Category Without Description"
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == category_data["title"]
    assert data["description"] is None


def test_read_categories(client: TestClient):
    # First create a category
    category_data = {
        "title": "Test Category",
        "description": "A test category"
    }
    client.post("/categories/", json=category_data)
    
    # Then read categories
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_category(client: TestClient):
    # First create a category
    category_data = {
        "title": "Test Category",
        "description": "A test category"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Then read the specific category
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["title"] == category_data["title"]


def test_update_category(client: TestClient):
    # First create a category
    category_data = {
        "title": "Test Category",
        "description": "A test category"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Then update the category
    update_data = {"title": "Updated Category"}
    response = client.put(f"/categories/{category_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Category"
    assert data["description"] == category_data["description"]  # Should remain unchanged


def test_delete_category(client: TestClient):
    # First create a category
    category_data = {
        "title": "Test Category",
        "description": "A test category"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Then delete the category
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    
    # Verify category is deleted
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 404


def test_read_nonexistent_category(client: TestClient):
    response = client.get("/categories/99999")
    assert response.status_code == 404


def test_update_nonexistent_category(client: TestClient):
    update_data = {"title": "Updated"}
    response = client.put("/categories/99999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_category(client: TestClient):
    response = client.delete("/categories/99999")
    assert response.status_code == 404