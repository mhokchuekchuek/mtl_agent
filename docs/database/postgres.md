# **🐘 PostgreSQL Database**

PostgreSQL database for long-term memory storage (LangGraph Store).


---


## **📍 Connection**

| Property | Value |
|----------|-------|
| Host | `localhost` |
| Port | `5432` |
| Database | `erp_agent` |
| User | `postgres` |


---


## **📊 Tables**

| Table | Description |
|-------|-------------|
| store | LangGraph Store for long-term memory |
| store_migrations | Migration tracking |


---


## **📋 Schema**


### 🗄️ **store**

LangGraph Store table for persistent memory across sessions.

| Column | Type | Description |
|--------|------|-------------|
| prefix | TEXT | Namespace prefix (e.g., `users/user-123`) |
| key | TEXT | Unique key within namespace |
| value | JSONB | Stored data (user preferences, facts, insights) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| expires_at | TIMESTAMP | Optional expiration time |
| ttl_minutes | INTEGER | Optional TTL in minutes |

**Indexes:**
- `store_pkey` - Primary key on (prefix, key)
- `idx_store_expires_at` - For TTL cleanup
- `store_prefix_idx` - For prefix lookups


---


## **💡 Usage**

```python
from libs.database.sql.selector import SQLSelector

db = SQLSelector.create(
    provider="postgres",
    host="localhost",
    port=5432,
    database="erp_agent",
    user="postgres",
    password="postgres"
)

# Query store
results = db.query("SELECT * FROM store WHERE prefix LIKE %s", ("users/%",))
```


---


## **🔗 Related**

- [Docker Setup](../infrastructure/docker/postgres.md)
- [PostgreSQL Client](../libs/database/sql/postgres.md)
- [Why Checkpointer + Store](../../decisions/why_checkpointer_and_store.md)
