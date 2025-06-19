from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
import database

app = FastAPI(title="Shop API", description="A simple shop API with FastAPI and SQLite", version="1.0.0")

# Error message constants
CUSTOMER_NOT_FOUND = "Customer not found"
CATEGORY_NOT_FOUND = "Category not found"
SHOP_ITEM_NOT_FOUND = "Shop item not found"
ORDER_NOT_FOUND = "Order not found"

# Create tables on startup
@app.on_event("startup")
def startup():
    database.create_tables()


# Customer endpoints
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    return crud.create_customer(db=db, customer=customer)


@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers


@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(database.get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail=CUSTOMER_NOT_FOUND)
    return db_customer


@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(database.get_db)):
    db_customer = crud.update_customer(db, customer_id=customer_id, customer=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail=CUSTOMER_NOT_FOUND)
    return db_customer


@app.delete("/customers/{customer_id}", response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(database.get_db)):
    db_customer = crud.delete_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail=CUSTOMER_NOT_FOUND)
    return db_customer


# ShopItemCategory endpoints
@app.post("/categories/", response_model=schemas.ShopItemCategory)
def create_category(category: schemas.ShopItemCategoryCreate, db: Session = Depends(database.get_db)):
    return crud.create_category(db=db, category=category)


@app.get("/categories/", response_model=List[schemas.ShopItemCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/categories/{category_id}", response_model=schemas.ShopItemCategory)
def read_category(category_id: int, db: Session = Depends(database.get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return db_category


@app.put("/categories/{category_id}", response_model=schemas.ShopItemCategory)
def update_category(category_id: int, category: schemas.ShopItemCategoryUpdate, db: Session = Depends(database.get_db)):
    db_category = crud.update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return db_category


@app.delete("/categories/{category_id}", response_model=schemas.ShopItemCategory)
def delete_category(category_id: int, db: Session = Depends(database.get_db)):
    db_category = crud.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return db_category


# ShopItem endpoints
@app.post("/shop-items/", response_model=schemas.ShopItem)
def create_shop_item(item: schemas.ShopItemCreate, db: Session = Depends(database.get_db)):
    return crud.create_shop_item(db=db, item=item)


@app.get("/shop-items/", response_model=List[schemas.ShopItem])
def read_shop_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = crud.get_shop_items(db, skip=skip, limit=limit)
    return items


@app.get("/shop-items/{item_id}", response_model=schemas.ShopItem)
def read_shop_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = crud.get_shop_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail=SHOP_ITEM_NOT_FOUND)
    return db_item


@app.put("/shop-items/{item_id}", response_model=schemas.ShopItem)
def update_shop_item(item_id: int, item: schemas.ShopItemUpdate, db: Session = Depends(database.get_db)):
    db_item = crud.update_shop_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail=SHOP_ITEM_NOT_FOUND)
    return db_item


@app.delete("/shop-items/{item_id}", response_model=schemas.ShopItem)
def delete_shop_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = crud.delete_shop_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail=SHOP_ITEM_NOT_FOUND)
    return db_item


# Order endpoints
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order(db=db, order=order)


@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(database.get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail=ORDER_NOT_FOUND)
    return db_order


@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(database.get_db)):
    db_order = crud.update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail=ORDER_NOT_FOUND)
    return db_order


@app.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(database.get_db)):
    db_order = crud.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail=ORDER_NOT_FOUND)
    return db_order


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
