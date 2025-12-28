# ERP Database

SQLite database containing ERP (Enterprise Resource Planning) data.

## Location

`data/erp_database.db`

## Tables

| Table | Description |
|-------|-------------|
| Products | Product catalog |
| Warehouses | Warehouse locations |
| Inventory | Stock levels by product/color/warehouse |
| Customers | Customer information |
| Suppliers | Supplier contacts |
| Orders | Order headers |
| OrderDetails | Order line items |

## Schema

### Products

| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Primary key |
| product_name | TEXT | Name of the product |
| product_type | TEXT | Type (e.g., Electronics, Home Appliances) |
| category | TEXT | Category of the product |
| price | INTEGER | Price in USD |

### Warehouses

| Column | Type | Description |
|--------|------|-------------|
| warehouse_id | INTEGER | Primary key |
| warehouse_name | TEXT | Name of the warehouse |
| location | TEXT | Location of the warehouse |

### Inventory

| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Reference to Products |
| color | TEXT | Color of the product |
| quantity | INTEGER | Quantity in stock |
| warehouse_id | INTEGER | Reference to Warehouses |

### Customers

| Column | Type | Description |
|--------|------|-------------|
| customer_id | INTEGER | Primary key |
| customer_name | TEXT | Name of the customer |
| email | TEXT | Email address |
| phone_number | TEXT | Phone number |
| address | TEXT | Address |

### Suppliers

| Column | Type | Description |
|--------|------|-------------|
| supplier_id | INTEGER | Primary key |
| supplier_name | TEXT | Name of the supplier |
| contact | TEXT | Contact information |
| address | TEXT | Address |

### Orders

| Column | Type | Description |
|--------|------|-------------|
| order_id | INTEGER | Primary key |
| order_date | TIMESTAMP | Date and time of order |
| customer_id | INTEGER | Reference to Customers |
| total_amount | INTEGER | Total order amount |

### OrderDetails

| Column | Type | Description |
|--------|------|-------------|
| order_detail_id | INTEGER | Primary key |
| order_id | INTEGER | Reference to Orders |
| product_id | INTEGER | Reference to Products |
| color | TEXT | Color of the product |
| quantity | INTEGER | Quantity ordered |
| price | INTEGER | Price per unit |
| total_price | INTEGER | Total price (quantity * price) |

## Usage

```python
from libs.database.sql.selector import SQLSelector

db = SQLSelector.create(
    provider="sqlite",
    db_path="data/erp_database.db"
)

# List tables
tables = db.get_tables()

# Query products
products = db.query("SELECT * FROM Products WHERE category = ?", ("Electronics",))
```
