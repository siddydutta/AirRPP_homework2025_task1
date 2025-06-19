from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional


# Customer CRUD
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        name=customer.name,
        surname=customer.surname,
        email=customer.email
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer


# ShopItemCategory CRUD
def get_category(db: Session, category_id: int):
    return db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShopItemCategory).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.ShopItemCategoryCreate):
    db_category = models.ShopItemCategory(
        title=category.title,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: schemas.ShopItemCategoryUpdate):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category:
        update_data = category.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


# ShopItem CRUD
def get_shop_item(db: Session, item_id: int):
    return db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()


def get_shop_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShopItem).offset(skip).limit(limit).all()


def create_shop_item(db: Session, item: schemas.ShopItemCreate):
    db_item = models.ShopItem(
        title=item.title,
        description=item.description,
        price=item.price
    )
    
    # Add categories
    if item.category_ids:
        categories = db.query(models.ShopItemCategory).filter(
            models.ShopItemCategory.id.in_(item.category_ids)
        ).all()
        db_item.categories = categories
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_shop_item(db: Session, item_id: int, item: schemas.ShopItemUpdate):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        
        # Handle category_ids separately
        if 'category_ids' in update_data:
            category_ids = update_data.pop('category_ids')
            if category_ids is not None:
                categories = db.query(models.ShopItemCategory).filter(
                    models.ShopItemCategory.id.in_(category_ids)
                ).all()
                db_item.categories = categories
        
        # Update other fields
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_shop_item(db: Session, item_id: int):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


# Order CRUD
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(customer_id=order.customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add order items
    for item in order.items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            shop_item_id=item.shop_item_id,
            quantity=item.quantity
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        update_data = order.model_dump(exclude_unset=True)
        
        # Handle items separately
        if 'items' in update_data:
            items = update_data.pop('items')
            if items is not None:
                # Delete existing order items
                db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
                
                # Add new order items
                for item in items:
                    db_order_item = models.OrderItem(
                        order_id=order_id,
                        shop_item_id=item['shop_item_id'],
                        quantity=item['quantity']
                    )
                    db.add(db_order_item)
        
        # Update other fields
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        # Ensure relationships are loaded before deletion
        _ = db_order.customer  # Trigger lazy loading
        _ = db_order.items  # Trigger lazy loading
        db.delete(db_order)
        db.commit()
    return db_order