#!/usr/bin/env python3
"""
Script to populate the database with initial data.
"""

import sys
import os
from sqlalchemy.orm import Session

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
import crud
import schemas


def create_initial_data():
    """Create initial data for the shop database."""
    
    # Create database tables
    database.create_tables()
    
    # Create database session
    db = Session(bind=database.engine)
    
    try:
        print("Creating initial data...")
        
        # Create customers
        customers_data = [
            {"name": "John", "surname": "Doe", "email": "john.doe@example.com"},
            {"name": "Jane", "surname": "Smith", "email": "jane.smith@example.com"},
            {"name": "Alice", "surname": "Johnson", "email": "alice.johnson@example.com"},
            {"name": "Bob", "surname": "Brown", "email": "bob.brown@example.com"},
        ]
        
        customers = []
        for customer_data in customers_data:
            customer = crud.create_customer(db, schemas.CustomerCreate(**customer_data))
            customers.append(customer)
            print(f"Created customer: {customer.name} {customer.surname}")
        
        # Create categories
        categories_data = [
            {"title": "Electronics", "description": "Electronic devices and gadgets"},
            {"title": "Books", "description": "Books and literature"},
            {"title": "Clothing", "description": "Clothing and apparel"},
            {"title": "Home & Garden", "description": "Home improvement and gardening items"},
            {"title": "Sports", "description": "Sports equipment and accessories"},
        ]
        
        categories = []
        for category_data in categories_data:
            category = crud.create_category(db, schemas.ShopItemCategoryCreate(**category_data))
            categories.append(category)
            print(f"Created category: {category.title}")
        
        # Create shop items
        shop_items_data = [
            {
                "title": "Smartphone",
                "description": "Latest model smartphone with advanced features",
                "price": 699.99,
                "category_ids": [categories[0].id]  # Electronics
            },
            {
                "title": "Laptop",
                "description": "High-performance laptop for work and gaming",
                "price": 1299.99,
                "category_ids": [categories[0].id]  # Electronics
            },
            {
                "title": "Python Programming Book",
                "description": "Comprehensive guide to Python programming",
                "price": 39.99,
                "category_ids": [categories[1].id]  # Books
            },
            {
                "title": "T-Shirt",
                "description": "Comfortable cotton t-shirt",
                "price": 19.99,
                "category_ids": [categories[2].id]  # Clothing
            },
            {
                "title": "Garden Hose",
                "description": "Durable garden hose for watering",
                "price": 29.99,
                "category_ids": [categories[3].id]  # Home & Garden
            },
            {
                "title": "Tennis Racket",
                "description": "Professional tennis racket",
                "price": 149.99,
                "category_ids": [categories[4].id]  # Sports
            },
            {
                "title": "Fitness Tracker",
                "description": "Waterproof fitness tracker with heart rate monitor",
                "price": 199.99,
                "category_ids": [categories[0].id, categories[4].id]  # Electronics & Sports
            },
        ]
        
        shop_items = []
        for item_data in shop_items_data:
            item = crud.create_shop_item(db, schemas.ShopItemCreate(**item_data))
            shop_items.append(item)
            print(f"Created shop item: {item.title} - ${item.price}")
        
        # Create orders
        orders_data = [
            {
                "customer_id": customers[0].id,
                "items": [
                    {"shop_item_id": shop_items[0].id, "quantity": 1},  # Smartphone
                    {"shop_item_id": shop_items[2].id, "quantity": 2},  # Python Book
                ]
            },
            {
                "customer_id": customers[1].id,
                "items": [
                    {"shop_item_id": shop_items[1].id, "quantity": 1},  # Laptop
                    {"shop_item_id": shop_items[6].id, "quantity": 1},  # Fitness Tracker
                ]
            },
            {
                "customer_id": customers[2].id,
                "items": [
                    {"shop_item_id": shop_items[3].id, "quantity": 3},  # T-Shirt
                    {"shop_item_id": shop_items[4].id, "quantity": 1},  # Garden Hose
                ]
            },
            {
                "customer_id": customers[3].id,
                "items": [
                    {"shop_item_id": shop_items[5].id, "quantity": 1},  # Tennis Racket
                ]
            },
        ]
        
        orders = []
        for order_data in orders_data:
            order = crud.create_order(db, schemas.OrderCreate(**order_data))
            orders.append(order)
            print(f"Created order for customer: {order.customer.name} {order.customer.surname}")
        
        print("\nInitial data creation completed successfully!")
        print(f"Created {len(customers)} customers")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(shop_items)} shop items")
        print(f"Created {len(orders)} orders")
        
    except Exception as e:
        print(f"Error creating initial data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
