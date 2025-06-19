from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models


def init_test_data():
    """Initialize the database with test data if it's empty."""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Customer).first() is not None:
            return
        
        # Create test customers
        customers = [
            models.Customer(name="John", surname="Doe", email="john.doe@example.com"),
            models.Customer(name="Jane", surname="Smith", email="jane.smith@example.com"),
            models.Customer(name="Bob", surname="Johnson", email="bob.johnson@example.com"),
        ]
        
        for customer in customers:
            db.add(customer)
        db.commit()
        
        # Create test categories
        categories = [
            models.ShopItemCategory(title="Electronics", description="Electronic devices and accessories"),
            models.ShopItemCategory(title="Books", description="Books and reading materials"),
            models.ShopItemCategory(title="Clothing", description="Clothing and fashion items"),
            models.ShopItemCategory(title="Home & Garden", description="Home and garden products"),
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Refresh to get IDs
        for category in categories:
            db.refresh(category)
        
        # Create test shop items
        shop_items = [
            models.ShopItem(
                title="Laptop",
                description="High-performance laptop for work and gaming",
                price=999.99
            ),
            models.ShopItem(
                title="Smartphone",
                description="Latest smartphone with advanced features",
                price=699.99
            ),
            models.ShopItem(
                title="Python Programming Book",
                description="Learn Python programming from scratch",
                price=29.99
            ),
            models.ShopItem(
                title="T-Shirt",
                description="Comfortable cotton t-shirt",
                price=19.99
            ),
            models.ShopItem(
                title="Coffee Mug",
                description="Ceramic coffee mug for your morning coffee",
                price=9.99
            ),
        ]
        
        for item in shop_items:
            db.add(item)
        db.commit()
        
        # Refresh to get IDs
        for item in shop_items:
            db.refresh(item)
        
        # Associate items with categories
        shop_items[0].categories.append(categories[0])  # Laptop -> Electronics
        shop_items[1].categories.append(categories[0])  # Smartphone -> Electronics
        shop_items[2].categories.append(categories[1])  # Book -> Books
        shop_items[3].categories.append(categories[2])  # T-Shirt -> Clothing
        shop_items[4].categories.append(categories[3])  # Coffee Mug -> Home & Garden
        
        db.commit()
        
        # Create test orders
        orders = [
            models.Order(customer_id=customers[0].id),
            models.Order(customer_id=customers[1].id),
        ]
        
        for order in orders:
            db.add(order)
        db.commit()
        
        # Refresh to get IDs
        for order in orders:
            db.refresh(order)
        
        # Create test order items
        order_items = [
            models.OrderItem(order_id=orders[0].id, shop_item_id=shop_items[0].id, quantity=1),  # John buys Laptop
            models.OrderItem(order_id=orders[0].id, shop_item_id=shop_items[4].id, quantity=2),  # John buys 2 Coffee Mugs
            models.OrderItem(order_id=orders[1].id, shop_item_id=shop_items[1].id, quantity=1),  # Jane buys Smartphone
            models.OrderItem(order_id=orders[1].id, shop_item_id=shop_items[2].id, quantity=1),  # Jane buys Book
        ]
        
        for order_item in order_items:
            db.add(order_item)
        db.commit()
        
        print("Test data initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing test data: {e}")
        db.rollback()
    finally:
        db.close()