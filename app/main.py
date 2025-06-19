from fastapi import FastAPI
from .database import create_tables
from .routers import customers, categories, shop_items, orders
from .init_data import init_test_data

app = FastAPI(title="Shop API", description="A simple shop API with FastAPI and SQLite", version="1.0.0")

# Create tables
create_tables()

# Initialize test data
init_test_data()

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(shop_items.router, prefix="/shop-items", tags=["shop-items"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Shop API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}