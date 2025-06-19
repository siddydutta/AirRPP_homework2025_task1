# Shop API

A simple shop API built with FastAPI, SQLAlchemy, and SQLite that provides full CRUD operations for managing customers, product categories, shop items, and orders.

## Features

- **Customer Management**: Create, read, update, and delete customers
- **Category Management**: Manage shop item categories
- **Shop Item Management**: Manage products with category associations
- **Order Management**: Create and manage orders with multiple items
- **Automatic Database Setup**: SQLite database with automatic table creation
- **Test Data Initialization**: Pre-populated with sample data for testing
- **Comprehensive Testing**: Full test suite for all endpoints
- **API Documentation**: Auto-generated interactive API docs

## Models

### Customer
- ID (integer, primary key)
- Name (string)
- Surname (string)
- Email (string, unique)

### ShopItemCategory
- ID (integer, primary key)
- Title (string)
- Description (string, optional)

### ShopItem
- ID (integer, primary key)
- Title (string)
- Description (string, optional)
- Price (float)
- Categories (many-to-many relationship with ShopItemCategory)

### Order
- ID (integer, primary key)
- Customer (foreign key to Customer)
- Items (list of OrderItem)

### OrderItem
- ID (integer, primary key)
- Order (foreign key to Order)
- ShopItem (foreign key to ShopItem)
- Quantity (integer)

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/siddy/Documents/projects/air-research-preview-program/task-1
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

### Available Endpoints

#### Customers
- `GET /customers/` - List all customers
- `POST /customers/` - Create a new customer
- `GET /customers/{customer_id}` - Get a specific customer
- `PUT /customers/{customer_id}` - Update a customer
- `DELETE /customers/{customer_id}` - Delete a customer

#### Categories
- `GET /categories/` - List all categories
- `POST /categories/` - Create a new category
- `GET /categories/{category_id}` - Get a specific category
- `PUT /categories/{category_id}` - Update a category
- `DELETE /categories/{category_id}` - Delete a category

#### Shop Items
- `GET /shop-items/` - List all shop items
- `POST /shop-items/` - Create a new shop item
- `GET /shop-items/{item_id}` - Get a specific shop item
- `PUT /shop-items/{item_id}` - Update a shop item
- `DELETE /shop-items/{item_id}` - Delete a shop item

#### Orders
- `GET /orders/` - List all orders
- `POST /orders/` - Create a new order
- `GET /orders/{order_id}` - Get a specific order
- `PUT /orders/{order_id}` - Update an order
- `DELETE /orders/{order_id}` - Delete an order

## Running Tests

The project includes comprehensive tests for all endpoints. To run the tests:

```bash
pytest
```

For more verbose output:
```bash
pytest -v
```

To run tests with coverage:
```bash
pytest --cov=app
```

To run specific test files:
```bash
pytest tests/test_customers.py
pytest tests/test_categories.py
pytest tests/test_shop_items.py
pytest tests/test_orders.py
```

## Test Data

The application automatically initializes with sample test data including:
- 3 customers (John Doe, Jane Smith, Bob Johnson)
- 4 categories (Electronics, Books, Clothing, Home & Garden)
- 5 shop items (Laptop, Smartphone, Python Book, T-Shirt, Coffee Mug)
- 2 sample orders with items

## Example API Usage

### Create a Customer
```bash
curl -X POST "http://localhost:8000/customers/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John",
       "surname": "Doe",
       "email": "john.doe@example.com"
     }'
```

### Create a Shop Item with Categories
```bash
curl -X POST "http://localhost:8000/shop-items/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Gaming Laptop",
       "description": "High-performance gaming laptop",
       "price": 1299.99,
       "category_ids": [1]
     }'
```

### Create an Order
```bash
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": 1,
       "items": [
         {
           "shop_item_id": 1,
           "quantity": 1
         },
         {
           "shop_item_id": 2,
           "quantity": 2
         }
       ]
     }'
```

## Database

The application uses SQLite as the database, which is automatically created as `shop.db` in the project root directory. The database schema is automatically created when the application starts.

For testing, a separate `test.db` file is used to ensure tests don't interfere with the main database.

## Development

### Project Structure
```
app/
├── __init__.py
├── main.py              # FastAPI application and startup
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for request/response
├── database.py          # Database configuration and connection
├── crud.py              # Database operations (Create, Read, Update, Delete)
├── init_data.py         # Test data initialization
└── routers/             # API route handlers
    ├── __init__.py
    ├── customers.py
    ├── categories.py
    ├── shop_items.py
    └── orders.py

tests/                   # Test suite
├── __init__.py
├── conftest.py          # Test configuration and fixtures
├── test_customers.py
├── test_categories.py
├── test_shop_items.py
└── test_orders.py
```

### Key Dependencies
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **Pytest**: Testing framework
- **HTTPx**: HTTP client for testing

## Contributing

1. Make sure all tests pass before submitting changes
2. Follow the existing code style and patterns
3. Add tests for any new functionality
4. Update documentation as needed

## License

This project is for educational purposes.