# **🗃️ SQLite Database**

SQLite database client for file-based SQL operations.


---


## **📍 Location**

[`libs/database/sql/sqlite/main.py`](../../../../libs/database/sql/sqlite/main.py)

---


## **📦 Class**

### `SQLiteClient`

SQLite database client with dictionary-style row access.


---


## **📋 Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_path` | str | - | Path to SQLite database file |

---


## **📋 Methods**


### `execute(query, params) -> int`

Execute a write query (INSERT, UPDATE, DELETE).

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | SQL query with ? placeholders |
| `params` | tuple | Parameter values |

**Returns**: Number of rows affected

### `query(query, params) -> list[dict]`

Execute a read query (SELECT).

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | SQL query with ? placeholders |
| `params` | tuple | Parameter values |

**Returns**: List of rows as dictionaries

### `get_tables() -> list[str]`

Get list of all table names in the database.

**Returns**: List of table names

### `get_schema(table_name) -> list[dict]`

Get schema information for a table.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `table_name` | str | Name of the table |

**Returns**: List of column info dictionaries with keys: `name`, `type`, `nullable`, `primary_key`

### `get_full_schema() -> dict`

Get schema for all tables (convenience method).

**Returns**: Dictionary mapping table names to their schemas

### `close() -> None`

Close the database connection.

---


## **🚀 Usage**

```python
from libs.database.sql.selector import SQLSelector

# Create SQLite client
db = SQLSelector.create(
    provider="sqlite",
    db_path="path/to/database.db"
)

# List tables
tables = db.get_tables()

# Query data
results = db.query(
    "SELECT * FROM users WHERE status = ?",
    ("active",)
)
print(results[0]["name"])

# Get schema
schema = db.get_schema("users")

# Execute write query
rows_affected = db.execute(
    "UPDATE users SET status = ? WHERE id = ?",
    ("inactive", 1)
)

# Use as context manager
with SQLSelector.create(provider="sqlite", db_path="path/to/database.db") as db:
    results = db.query("SELECT COUNT(*) as count FROM users")
    print(results[0]["count"])
```
