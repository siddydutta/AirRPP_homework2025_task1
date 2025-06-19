import pytest
from fastapi.testclient import TestClient


def test_create_shop_item(client: TestClient):
    # First create a category
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices"
    }
    category_response = client.post("/categories/", json=category_data)
    category_id = category_response.json()["id"]
    
    # Then create a shop item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99,
        "category_ids": [category_id]
    }
    response = client.post("/shop-items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert len(data["categories"]) == 1
    assert data["categories"][0]["id"] == category_id
    assert "id" in data


def test_create_shop_item_without_categories(client: TestClient):
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99
    }
    response = client.post("/shop-items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["categories"] == []


def test_read_shop_items(client: TestClient):
    # First create a shop item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99
    }
    client.post("/shop-items/", json=item_data)
    
    # Then read shop items
    response = client.get("/shop-items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_shop_item(client: TestClient):
    # First create a shop item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99
    }
    create_response = client.post("/shop-items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Then read the specific shop item
    response = client.get(f"/shop-items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]


def test_update_shop_item(client: TestClient):
    # First create a shop item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99
    }
    create_response = client.post("/shop-items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Then update the shop item
    update_data = {"title": "Updated Item", "price": 199.99}
    response = client.put(f"/shop-items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"
    assert data["price"] == 199.99
    assert data["description"] == item_data["description"]  # Should remain unchanged


def test_update_shop_item_categories(client: TestClient):
    # First create categories
    category1_data = {"title": "Category 1", "description": "First category"}
    category2_data = {"title": "Category 2", "description": "Second category"}
    
    category1_response = client.post("/categories/", json=category1_data)
    category2_response = client.post("/categories/", json=category2_data)
    
    category1_id = category1_response.json()["id"]
    category2_id = category2_response.json()["id"]
    
    # Create a shop item with one category
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99,
        "category_ids": [category1_id]
    }
    create_response = client.post("/shop-items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Update the item with different categories
    update_data = {"category_ids": [category2_id]}
    response = client.put(f"/shop-items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["categories"]) == 1
    assert data["categories"][0]["id"] == category2_id


def test_delete_shop_item(client: TestClient):
    # First create a shop item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 99.99
    }
    create_response = client.post("/shop-items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Then delete the shop item
    response = client.delete(f"/shop-items/{item_id}")
    assert response.status_code == 200
    
    # Verify shop item is deleted
    response = client.get(f"/shop-items/{item_id}")
    assert response.status_code == 404


def test_read_nonexistent_shop_item(client: TestClient):
    response = client.get("/shop-items/99999")
    assert response.status_code == 404


def test_update_nonexistent_shop_item(client: TestClient):
    update_data = {"title": "Updated"}
    response = client.put("/shop-items/99999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_shop_item(client: TestClient):
    response = client.delete("/shop-items/99999")
    assert response.status_code == 404