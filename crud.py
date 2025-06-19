from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import database
import schemas


# Customer CRUD operations
def get_customer(db: Session, customer_id: int):
    return db.query(database.Customer).filter(database.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = database.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer


# ShopItemCategory CRUD operations
def get_category(db: Session, category_id: int):
    return db.query(database.ShopItemCategory).filter(database.ShopItemCategory.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.ShopItemCategory).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.ShopItemCategoryCreate):
    db_category = database.ShopItemCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: schemas.ShopItemCategoryUpdate):
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


# ShopItem CRUD operations
def get_shop_item(db: Session, item_id: int):
    return db.query(database.ShopItem).filter(database.ShopItem.id == item_id).first()


def get_shop_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.ShopItem).offset(skip).limit(limit).all()


def create_shop_item(db: Session, item: schemas.ShopItemCreate):
    # Create shop item without categories first
    item_data = item.dict()
    category_ids = item_data.pop('category_ids', [])
    
    db_item = database.ShopItem(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Add categories if provided
    if category_ids:
        categories = db.query(database.ShopItemCategory).filter(database.ShopItemCategory.id.in_(category_ids)).all()
        db_item.categories = categories
        db.commit()
        db.refresh(db_item)
    
    return db_item


def update_shop_item(db: Session, item_id: int, item: schemas.ShopItemUpdate):
    db_item = get_shop_item(db, item_id)
    if db_item:
        update_data = item.dict(exclude_unset=True)
        category_ids = update_data.pop('category_ids', None)
        
        # Update basic fields
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        # Update categories if provided
        if category_ids is not None:
            categories = db.query(database.ShopItemCategory).filter(database.ShopItemCategory.id.in_(category_ids)).all()
            db_item.categories = categories
        
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_shop_item(db: Session, item_id: int):
    db_item = get_shop_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


# Order CRUD operations
def get_order(db: Session, order_id: int):
    return db.query(database.Order).filter(database.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate):
    # Create order first
    order_data = order.dict()
    items_data = order_data.pop('items', [])
    
    db_order = database.Order(**order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add order items
    for item_data in items_data:
        db_order_item = database.OrderItem(**item_data, order_id=db_order.id)
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = get_order(db, order_id)
    if db_order:
        update_data = order.dict(exclude_unset=True)
        items_data = update_data.pop('items', None)
        
        # Update basic fields
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        # Update items if provided
        if items_data is not None:
            # Delete existing order items
            db.query(database.OrderItem).filter(database.OrderItem.order_id == order_id).delete()
            
            # Add new order items
            for item_data in items_data:
                db_order_item = database.OrderItem(**item_data, order_id=order_id)
                db.add(db_order_item)
        
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        # Eagerly load relationships before deletion to avoid session issues
        customer = db_order.customer
        items = []
        for item in db_order.items:
            # Trigger loading of the shop_item relationship while session is active
            _ = item.shop_item
            items.append(item)
        
        # Delete order items first (cascade should handle this, but let's be explicit)
        db.query(database.OrderItem).filter(database.OrderItem.order_id == order_id).delete()
        db.delete(db_order)
        db.commit()
        
        # Create a detached copy for return
        result_order = database.Order(id=db_order.id, customer_id=db_order.customer_id)
        result_order.customer = customer
        result_order.items = items
        return result_order
    return db_order
