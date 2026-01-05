# **🗄️ ERP Database**

SQLite database containing ERP (Enterprise Resource Planning) data.


---


## **📍 Location**

[`data/erp_database.db`](../../../data/erp_database.db)


---


## **📊 Tables**

| Table | Description |
|-------|-------------|
| Products | Product catalog |
| Warehouses | Warehouse locations |
| Inventory | Stock levels by product/color/warehouse |
| Customers | Customer information |
| Suppliers | Supplier contacts |
| Orders | Order headers |
| OrderDetails | Order line items |
| _migrations | Migration tracking |


---


## **📋 Schema**


### 🛍️ **Products**

Product catalog with 100 items across various categories.

| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Primary key |
| product_name | TEXT | Name of the product (e.g., "Espresso Coffee Maker") |
| product_type | TEXT | Type (e.g., "Home Appliances", "Electronics") |
| category | TEXT | Category (e.g., "Home & Kitchen", "Gadgets & Electronics") |
| price | INTEGER | Price in USD |


### 🏭 **Warehouses**

Warehouse locations for inventory storage.

| Column | Type | Description |
|--------|------|-------------|
| warehouse_id | INTEGER | Primary key |
| warehouse_name | TEXT | Name of the warehouse (e.g., "Main Warehouse") |
| location | TEXT | City location (e.g., "New York", "Los Angeles") |


### 📦 **Inventory**

Stock levels by product, color, and warehouse.

| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Reference to Products |
| color | TEXT | Color variant (e.g., "Black", "White") |
| quantity | INTEGER | Quantity in stock |
| warehouse_id | INTEGER | Reference to Warehouses |


### 👤 **Customers**

Customer information for order tracking and communication.

| Column | Type | Description |
|--------|------|-------------|
| customer_id | INTEGER | Primary key |
| customer_name | TEXT | Full name (e.g., "Brenda Ross") |
| email | TEXT | Email address |
| phone_number | TEXT | Phone number with country code |
| address | TEXT | Full address |


### 🚚 **Suppliers**

Supplier contacts for product sourcing.

| Column | Type | Description |
|--------|------|-------------|
| supplier_id | INTEGER | Primary key |
| supplier_name | TEXT | Company name (e.g., "Tech Supplies Inc.") |
| contact | TEXT | Email address |
| address | TEXT | Full address |


### 📝 **Orders**

Order headers with customer reference and total amount.

| Column | Type | Description |
|--------|------|-------------|
| order_id | INTEGER | Primary key (auto-increment) |
| order_date | TIMESTAMP | Date and time of order |
| customer_id | INTEGER | Reference to Customers |
| total_amount | INTEGER | Total order amount in USD |
| status | TEXT | Order status (default: "completed") |

**Status Values:**

| Status | Description |
|--------|-------------|
| `pending` | Order placed, awaiting processing |
| `completed` | Order processed/shipped |
| `cancelled` | Order cancelled by customer |
| `refunded` | Order refunded |


### 📋 **OrderDetails**

Order line items with product, quantity, and price.

| Column | Type | Description |
|--------|------|-------------|
| order_detail_id | INTEGER | Primary key |
| order_id | INTEGER | Reference to Orders |
| product_id | INTEGER | Reference to Products |
| color | TEXT | Color variant ordered |
| quantity | INTEGER | Quantity ordered |
| price | INTEGER | Price per unit in USD |
| total_price | INTEGER | Total price (quantity * price) |


---


### 🔄 **_migrations**

Migration tracking for database schema changes. Managed by `scripts/run_migrations.sh`.

| Column | Type | Description |
|--------|------|-------------|
| name | TEXT | Migration filename (primary key) |
| applied_at | TIMESTAMP | When migration was applied |

**Applied Migrations:**

| Migration | Description |
|-----------|-------------|
| `001_add_order_status.sql` | Add status column to Orders table |
| `002_fix_orders_primary_key.sql` | Fix Orders PRIMARY KEY AUTOINCREMENT |


---


## **💡 Usage**

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
