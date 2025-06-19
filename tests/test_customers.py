import pytest
from fastapi.testclient import TestClient


def test_create_customer(client: TestClient):
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["surname"] == customer_data["surname"]
    assert data["email"] == customer_data["email"]
    assert "id" in data


def test_read_customers(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    client.post("/customers/", json=customer_data)
    
    # Then read customers
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_customer(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test2@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Then read the specific customer
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == customer_data["name"]


def test_update_customer(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test3@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Then update the customer
    update_data = {"name": "Updated"}
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["surname"] == customer_data["surname"]  # Should remain unchanged


def test_delete_customer(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test4@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Then delete the customer
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    
    # Verify customer is deleted
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404


def test_read_nonexistent_customer(client: TestClient):
    response = client.get("/customers/99999")
    assert response.status_code == 404


def test_update_nonexistent_customer(client: TestClient):
    update_data = {"name": "Updated"}
    response = client.put("/customers/99999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_customer(client: TestClient):
    response = client.delete("/customers/99999")
    assert response.status_code == 404