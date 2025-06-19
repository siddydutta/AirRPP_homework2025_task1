from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table for many-to-many relationship between ShopItem and ShopItemCategory
shop_item_category_association = Table(
    'shop_item_category_association',
    Base.metadata,
    Column('shop_item_id', Integer, ForeignKey('shop_items.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('shop_item_categories.id'), primary_key=True)
)


class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Relationship
    orders = relationship("Order", back_populates="customer")


class ShopItemCategory(Base):
    __tablename__ = 'shop_item_categories'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    
    # Relationship
    shop_items = relationship("ShopItem", secondary=shop_item_category_association, back_populates="categories")


class ShopItem(Base):
    __tablename__ = 'shop_items'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    
    # Relationships
    categories = relationship("ShopItemCategory", secondary=shop_item_category_association, back_populates="shop_items")
    order_items = relationship("OrderItem", back_populates="shop_item")


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    shop_item_id = Column(Integer, ForeignKey('shop_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    shop_item = relationship("ShopItem", back_populates="order_items")