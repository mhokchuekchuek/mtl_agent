# **🔷 SQL Database**

SQL database implementations using the provider/selector pattern.


---


## **📍 Location**

[`libs/database/sql/`](../../../../libs/database/sql/)


---


## **📦 Providers**

| Provider | Description | Documentation | Registered |
|----------|-------------|---------------|------------|
| `sqlite` | SQLite database | [sqlite.md](sqlite.md) | Yes |
| `postgres` | PostgreSQL database | [postgres.md](postgres.md) | No (use directly) |


---


## **🔧 Classes**


### 🎯 **BaseSQLDatabase**

Abstract base class for SQL databases.

**Location**: `libs/database/sql/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `execute(query, params)` | Execute write queries (INSERT/UPDATE/DELETE) |
| `query(query, params)` | Execute read queries (SELECT) |
| `get_tables()` | List all table names |
| `get_schema(table_name)` | Get column info for a table |
| `get_db_type()` | Get database type identifier (e.g., "sqlite", "postgresql") |


### 🔀 **SQLSelector**

Selector for SQL database providers.

**Location**: `libs/database/sql/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create SQL database instance |
| `list_providers()` | List available providers |


---


## **💡 Usage**

```python
from libs.database.sql.selector import SQLSelector

# Create SQLite client
db = SQLSelector.create(
    provider="sqlite",
    db_path="data/erp_database.db"
)

# List tables
tables = db.get_tables()

# Query data
products = db.query("SELECT * FROM Products WHERE category = ?", ("Electronics",))

# Get schema
schema = db.get_schema("Products")
```
