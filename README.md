# Shop API

A FastAPI-based REST API for managing a simple e-commerce shop with SQLite database.

## Features

- **Customer Management**: Create, read, update, and delete customers
- **Category Management**: Manage shop item categories
- **Shop Item Management**: Manage products with categories and pricing
- **Order Management**: Create and manage orders with multiple items
- **Database**: SQLite database with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite with pytest

## Models

### Customer
- ID (integer, primary key)
- Name (string)
- Surname (string)
- Email (string, unique)

### ShopItemCategory
- ID (integer, primary key)
- Title (string)
- Description (string)

### ShopItem
- ID (integer, primary key)
- Title (string)
- Description (string)
- Price (float)
- Categories (many-to-many relationship with ShopItemCategory)

### OrderItem
- ID (integer, primary key)
- ShopItem (foreign key to ShopItem)
- Quantity (integer)
- Order (foreign key to Order)

### Order
- ID (integer, primary key)
- Customer (foreign key to Customer)
- Items (one-to-many relationship with OrderItem)

## API Endpoints

### Customers
- `POST /customers/` - Create a new customer
- `GET /customers/` - List all customers (with pagination)
- `GET /customers/{id}` - Get customer by ID
- `PUT /customers/{id}` - Update customer
- `DELETE /customers/{id}` - Delete customer

### Categories
- `POST /categories/` - Create a new category
- `GET /categories/` - List all categories (with pagination)
- `GET /categories/{id}` - Get category by ID
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

### Shop Items
- `POST /shop-items/` - Create a new shop item
- `GET /shop-items/` - List all shop items (with pagination)
- `GET /shop-items/{id}` - Get shop item by ID
- `PUT /shop-items/{id}` - Update shop item
- `DELETE /shop-items/{id}` - Delete shop item

### Orders
- `POST /orders/` - Create a new order
- `GET /orders/` - List all orders (with pagination)
- `GET /orders/{id}` - Get order by ID
- `PUT /orders/{id}` - Update order
- `DELETE /orders/{id}` - Delete order

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database with sample data (optional):**
   ```bash
   python init_data.py
   ```

## Running the Application

### Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with verbose output:
```bash
pytest -v
```

### Run tests with coverage:
```bash
pytest --cov=. --cov-report=html
```

### Run specific test classes:
```bash
pytest test_main.py::TestCustomers -v
pytest test_main.py::TestCategories -v
pytest test_main.py::TestShopItems -v
pytest test_main.py::TestOrders -v
```

## Project Structure

```
.
├── main.py              # FastAPI application and route definitions
├── database.py          # Database configuration and models
├── schemas.py           # Pydantic schemas for request/response validation
├── crud.py              # Database CRUD operations
├── init_data.py         # Script to populate database with initial data
├── test_main.py         # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── shop.db             # SQLite database file (created when app runs)
└── test.db             # Test database file (created during testing)
```

## Usage Examples

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

### Create a Category
```bash
curl -X POST "http://localhost:8000/categories/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Electronics",
       "description": "Electronic devices and gadgets"
     }'
```

### Create a Shop Item with Categories
```bash
curl -X POST "http://localhost:8000/shop-items/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Smartphone",
       "description": "Latest model smartphone",
       "price": 699.99,
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
           "quantity": 2
         }
       ]
     }'
```

### Get All Customers
```bash
curl "http://localhost:8000/customers/"
```

### Get Customer by ID
```bash
curl "http://localhost:8000/customers/1"
```

## Database Schema

The application uses SQLite with the following relationships:
- **Customers** have many **Orders**
- **Orders** have many **OrderItems**
- **OrderItems** reference **ShopItems**
- **ShopItems** have many-to-many relationship with **ShopItemCategories**

## Testing Strategy

The test suite includes:
- **Unit tests** for each CRUD operation
- **Integration tests** for complete workflows
- **Error handling tests** for invalid requests
- **Edge cases** like empty orders, non-existent resources, etc.

Tests use a separate SQLite database (`test.db`) that is created and destroyed for each test run to ensure test isolation.

## Development

### Adding New Features
1. Update models in `database.py`
2. Add corresponding schemas in `schemas.py`
3. Implement CRUD operations in `crud.py`
4. Add API endpoints in `main.py`
5. Write tests in `test_main.py`

### Database Migrations
Currently, the application uses SQLAlchemy's `create_all()` method. For production use, consider implementing proper database migrations using Alembic.

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `main.py` or kill the process using port 8000
2. **Database locked**: Make sure no other instances of the application are running
3. **Import errors**: Ensure all dependencies are installed and the virtual environment is activated

### Logs
The application logs are displayed in the console. For production deployment, consider configuring proper logging to files.

## License

This project is for educational purposes. Feel free to modify and use as needed.
