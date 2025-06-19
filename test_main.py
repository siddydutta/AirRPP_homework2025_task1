import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


# Sample data fixtures
@pytest.fixture
def sample_customer():
    return {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }


@pytest.fixture
def sample_category():
    return {
        "title": "Electronics",
        "description": "Electronic devices and gadgets"
    }


@pytest.fixture
def sample_shop_item():
    return {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 699.99,
        "category_ids": []
    }


# Customer Tests
class TestCustomers:
    
    def test_create_customer(self, client, sample_customer):
        response = client.post("/customers/", json=sample_customer)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_customer["name"]
        assert data["surname"] == sample_customer["surname"]
        assert data["email"] == sample_customer["email"]
        assert "id" in data
    
    def test_read_customers(self, client, sample_customer):
        # Create a customer first
        client.post("/customers/", json=sample_customer)
        
        response = client.get("/customers/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == sample_customer["name"]
    
    def test_read_customer_by_id(self, client, sample_customer):
        # Create a customer first
        create_response = client.post("/customers/", json=sample_customer)
        customer_id = create_response.json()["id"]
        
        response = client.get(f"/customers/{customer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == customer_id
        assert data["name"] == sample_customer["name"]
    
    def test_read_customer_not_found(self, client):
        response = client.get("/customers/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
    
    def test_update_customer(self, client, sample_customer):
        # Create a customer first
        create_response = client.post("/customers/", json=sample_customer)
        customer_id = create_response.json()["id"]
        
        update_data = {"name": "Jane", "email": "jane.doe@example.com"}
        response = client.put(f"/customers/{customer_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane"
        assert data["email"] == "jane.doe@example.com"
        assert data["surname"] == sample_customer["surname"]  # Unchanged
    
    def test_update_customer_not_found(self, client):
        update_data = {"name": "Jane"}
        response = client.put("/customers/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_customer(self, client, sample_customer):
        # Create a customer first
        create_response = client.post("/customers/", json=sample_customer)
        customer_id = create_response.json()["id"]
        
        response = client.delete(f"/customers/{customer_id}")
        assert response.status_code == 200
        
        # Verify customer is deleted
        get_response = client.get(f"/customers/{customer_id}")
        assert get_response.status_code == 404
    
    def test_delete_customer_not_found(self, client):
        response = client.delete("/customers/999")
        assert response.status_code == 404


# Category Tests
class TestCategories:
    
    def test_create_category(self, client, sample_category):
        response = client.post("/categories/", json=sample_category)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_category["title"]
        assert data["description"] == sample_category["description"]
        assert "id" in data
    
    def test_read_categories(self, client, sample_category):
        # Create a category first
        client.post("/categories/", json=sample_category)
        
        response = client.get("/categories/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == sample_category["title"]
    
    def test_read_category_by_id(self, client, sample_category):
        # Create a category first
        create_response = client.post("/categories/", json=sample_category)
        category_id = create_response.json()["id"]
        
        response = client.get(f"/categories/{category_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["title"] == sample_category["title"]
    
    def test_read_category_not_found(self, client):
        response = client.get("/categories/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"
    
    def test_update_category(self, client, sample_category):
        # Create a category first
        create_response = client.post("/categories/", json=sample_category)
        category_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Electronics", "description": "Updated description"}
        response = client.put(f"/categories/{category_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Electronics"
        assert data["description"] == "Updated description"
    
    def test_update_category_not_found(self, client):
        update_data = {"title": "Updated"}
        response = client.put("/categories/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_category(self, client, sample_category):
        # Create a category first
        create_response = client.post("/categories/", json=sample_category)
        category_id = create_response.json()["id"]
        
        response = client.delete(f"/categories/{category_id}")
        assert response.status_code == 200
        
        # Verify category is deleted
        get_response = client.get(f"/categories/{category_id}")
        assert get_response.status_code == 404
    
    def test_delete_category_not_found(self, client):
        response = client.delete("/categories/999")
        assert response.status_code == 404


# Shop Item Tests
class TestShopItems:
    
    def test_create_shop_item(self, client, sample_shop_item):
        response = client.post("/shop-items/", json=sample_shop_item)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_shop_item["title"]
        assert data["description"] == sample_shop_item["description"]
        assert data["price"] == sample_shop_item["price"]
        assert "id" in data
    
    def test_create_shop_item_with_categories(self, client, sample_category):
        # Create a category first
        category_response = client.post("/categories/", json=sample_category)
        category_id = category_response.json()["id"]
        
        shop_item_data = {
            "title": "Smartphone",
            "description": "Latest model smartphone",
            "price": 699.99,
            "category_ids": [category_id]
        }
        
        response = client.post("/shop-items/", json=shop_item_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 1
        assert data["categories"][0]["id"] == category_id
    
    def test_read_shop_items(self, client, sample_shop_item):
        # Create a shop item first
        client.post("/shop-items/", json=sample_shop_item)
        
        response = client.get("/shop-items/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == sample_shop_item["title"]
    
    def test_read_shop_item_by_id(self, client, sample_shop_item):
        # Create a shop item first
        create_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = create_response.json()["id"]
        
        response = client.get(f"/shop-items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["title"] == sample_shop_item["title"]
    
    def test_read_shop_item_not_found(self, client):
        response = client.get("/shop-items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Shop item not found"
    
    def test_update_shop_item(self, client, sample_shop_item):
        # Create a shop item first
        create_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Smartphone", "price": 799.99}
        response = client.put(f"/shop-items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Smartphone"
        assert abs(data["price"] - 799.99) < 0.01
        assert data["description"] == sample_shop_item["description"]  # Unchanged
    
    def test_update_shop_item_not_found(self, client):
        update_data = {"title": "Updated"}
        response = client.put("/shop-items/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_shop_item(self, client, sample_shop_item):
        # Create a shop item first
        create_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = create_response.json()["id"]
        
        response = client.delete(f"/shop-items/{item_id}")
        assert response.status_code == 200
        
        # Verify shop item is deleted
        get_response = client.get(f"/shop-items/{item_id}")
        assert get_response.status_code == 404
    
    def test_delete_shop_item_not_found(self, client):
        response = client.delete("/shop-items/999")
        assert response.status_code == 404


# Order Tests
class TestOrders:
    
    def test_create_order(self, client, sample_customer, sample_shop_item):
        # Create customer and shop item first
        customer_response = client.post("/customers/", json=sample_customer)
        customer_id = customer_response.json()["id"]
        
        item_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = item_response.json()["id"]
        
        order_data = {
            "customer_id": customer_id,
            "items": [
                {"shop_item_id": item_id, "quantity": 2}
            ]
        }
        
        response = client.post("/orders/", json=order_data)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == customer_id
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 2
        assert "id" in data
    
    def test_create_order_empty_items(self, client, sample_customer):
        # Create customer first
        customer_response = client.post("/customers/", json=sample_customer)
        customer_id = customer_response.json()["id"]
        
        order_data = {
            "customer_id": customer_id,
            "items": []
        }
        
        response = client.post("/orders/", json=order_data)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == customer_id
        assert len(data["items"]) == 0
    
    def test_read_orders(self, client, sample_customer, sample_shop_item):
        # Create customer and shop item first
        customer_response = client.post("/customers/", json=sample_customer)
        customer_id = customer_response.json()["id"]
        
        item_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = item_response.json()["id"]
        
        order_data = {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 1}]
        }
        client.post("/orders/", json=order_data)
        
        response = client.get("/orders/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["customer_id"] == customer_id
    
    def test_read_order_by_id(self, client, sample_customer, sample_shop_item):
        # Create customer and shop item first
        customer_response = client.post("/customers/", json=sample_customer)
        customer_id = customer_response.json()["id"]
        
        item_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = item_response.json()["id"]
        
        order_data = {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 1}]
        }
        create_response = client.post("/orders/", json=order_data)
        order_id = create_response.json()["id"]
        
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id
        assert data["customer_id"] == customer_id
    
    def test_read_order_not_found(self, client):
        response = client.get("/orders/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Order not found"
    
    def test_update_order(self, client, sample_customer, sample_shop_item):
        # Create customer and shop item first
        customer_response = client.post("/customers/", json=sample_customer)
        customer_id = customer_response.json()["id"]
        
        item_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = item_response.json()["id"]
        
        order_data = {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 1}]
        }
        create_response = client.post("/orders/", json=order_data)
        order_id = create_response.json()["id"]
        
        update_data = {
            "items": [{"shop_item_id": item_id, "quantity": 3}]
        }
        response = client.put(f"/orders/{order_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 3
    
    def test_update_order_not_found(self, client):
        update_data = {"items": []}
        response = client.put("/orders/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_order(self, client, sample_customer, sample_shop_item):
        # Create customer and shop item first
        customer_response = client.post("/customers/", json=sample_customer)
        customer_id = customer_response.json()["id"]
        
        item_response = client.post("/shop-items/", json=sample_shop_item)
        item_id = item_response.json()["id"]
        
        order_data = {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 1}]
        }
        create_response = client.post("/orders/", json=order_data)
        order_id = create_response.json()["id"]
        
        response = client.delete(f"/orders/{order_id}")
        assert response.status_code == 200
        
        # Verify order is deleted
        get_response = client.get(f"/orders/{order_id}")
        assert get_response.status_code == 404
    
    def test_delete_order_not_found(self, client):
        response = client.delete("/orders/999")
        assert response.status_code == 404


# Integration Tests
class TestIntegration:
    
    def test_complete_workflow(self, client):
        """Test a complete workflow: create customer, category, shop item, and order"""
        
        # Create customer
        customer_data = {"name": "Alice", "surname": "Wonder", "email": "alice@example.com"}
        customer_response = client.post("/customers/", json=customer_data)
        customer_id = customer_response.json()["id"]
        
        # Create category
        category_data = {"title": "Books", "description": "Educational books"}
        category_response = client.post("/categories/", json=category_data)
        category_id = category_response.json()["id"]
        
        # Create shop item with category
        item_data = {
            "title": "Python Guide",
            "description": "Complete Python programming guide",
            "price": 49.99,
            "category_ids": [category_id]
        }
        item_response = client.post("/shop-items/", json=item_data)
        item_id = item_response.json()["id"]
        
        # Verify shop item has category
        item_get_response = client.get(f"/shop-items/{item_id}")
        item_data_with_category = item_get_response.json()
        assert len(item_data_with_category["categories"]) == 1
        assert item_data_with_category["categories"][0]["title"] == "Books"
        
        # Create order
        order_data = {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 2}]
        }
        order_response = client.post("/orders/", json=order_data)
        order_id = order_response.json()["id"]
        
        # Verify order details
        order_get_response = client.get(f"/orders/{order_id}")
        order_details = order_get_response.json()
        assert order_details["customer"]["name"] == "Alice"
        assert len(order_details["items"]) == 1
        assert order_details["items"][0]["shop_item"]["title"] == "Python Guide"
        assert order_details["items"][0]["quantity"] == 2
