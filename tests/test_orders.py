import pytest
from fastapi.testclient import TestClient


def test_create_order(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "Customer",
        "email": "test.customer@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create a shop item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99
    }
    item_response = client.post("/shop-items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Then create an order
    order_data = {
        "customer_id": customer_id,
        "items": [
            {
                "shop_item_id": item_id,
                "quantity": 2
            }
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert len(data["items"]) == 1
    assert data["items"][0]["shop_item_id"] == item_id
    assert data["items"][0]["quantity"] == 2
    assert "id" in data


def test_create_order_without_items(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "Customer",
        "email": "test.customer2@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create an order without items
    order_data = {
        "customer_id": customer_id
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["items"] == []


def test_read_orders(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "Customer",
        "email": "test.customer3@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create an order
    order_data = {
        "customer_id": customer_id
    }
    client.post("/orders/", json=order_data)
    
    # Then read orders
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_order(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "Customer",
        "email": "test.customer4@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create an order
    order_data = {
        "customer_id": customer_id
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Then read the specific order
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_id"] == customer_id


def test_update_order(client: TestClient):
    # First create customers
    customer1_data = {
        "name": "Test",
        "surname": "Customer1",
        "email": "test.customer5@example.com"
    }
    customer2_data = {
        "name": "Test",
        "surname": "Customer2",
        "email": "test.customer6@example.com"
    }
    customer1_response = client.post("/customers/", json=customer1_data)
    customer2_response = client.post("/customers/", json=customer2_data)
    customer1_id = customer1_response.json()["id"]
    customer2_id = customer2_response.json()["id"]
    
    # Create shop items
    item1_data = {"title": "Item 1", "price": 10.0}
    item2_data = {"title": "Item 2", "price": 20.0}
    item1_response = client.post("/shop-items/", json=item1_data)
    item2_response = client.post("/shop-items/", json=item2_data)
    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]
    
    # Create an order
    order_data = {
        "customer_id": customer1_id,
        "items": [{"shop_item_id": item1_id, "quantity": 1}]
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update the order
    update_data = {
        "customer_id": customer2_id,
        "items": [{"shop_item_id": item2_id, "quantity": 3}]
    }
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer2_id
    assert len(data["items"]) == 1
    assert data["items"][0]["shop_item_id"] == item2_id
    assert data["items"][0]["quantity"] == 3


def test_delete_order(client: TestClient):
    # First create a customer
    customer_data = {
        "name": "Test",
        "surname": "Customer",
        "email": "test.customer7@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create an order
    order_data = {
        "customer_id": customer_id
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Then delete the order
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    
    # Verify order is deleted
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404


def test_read_nonexistent_order(client: TestClient):
    response = client.get("/orders/99999")
    assert response.status_code == 404


def test_update_nonexistent_order(client: TestClient):
    update_data = {"customer_id": 1}
    response = client.put("/orders/99999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_order(client: TestClient):
    response = client.delete("/orders/99999")
    assert response.status_code == 404