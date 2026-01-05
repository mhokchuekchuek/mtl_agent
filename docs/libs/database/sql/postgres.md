# **🐘 PostgreSQLClient**

PostgreSQL database client implementing `BaseSQLDatabase` interface.


---


## **📍 Location**

[`libs/database/sql/postgres/main.py`](../../../libs/database/sql/postgres/main.py)

---


## **🚀 Usage**

```python
from libs.database.sql.postgres.main import PostgreSQLClient

client = PostgreSQLClient(
    host="localhost",
    port=5432,
    database="mydb",
    user="postgres",
    password="secret"
)

# Query data
results = client.query("SELECT * FROM users WHERE id = %s", (1,))

# Get table list
tables = client.get_tables()

# Get table schema
schema = client.get_schema("users")
```

---


## **📋 Methods**

### `query(query: str, params: tuple = ()) -> list[dict]`
Execute SELECT query and return results as list of dictionaries.

### `get_tables() -> list[str]`
Get list of all tables in the database.

### `get_schema(table_name: str) -> list[dict]`
Get column information for a table including:
- column_name
- data_type
- is_nullable
- is_primary_key

---


## **📦 Dependencies**

- `psycopg[binary]` - PostgreSQL adapter
