# **🗄️ PostgresStoreRepository**

PostgreSQL-based store for long-term memory.


---


## **📍 Location**

[`src/repositories/stores/postgres/main.py`](../../../../../src/repositories/stores/postgres/main.py)

---


## **💡 Purpose**

Provide permanent storage for conversation data using LangGraph's PostgresStore.


---


## **🔄 Code Flow**

![Code Flow](../../../../assets/diagrams/repositories/postgres_main_1.png)


---


## **📋 Class Definition**

```python
class PostgresStoreRepository(BaseStoreRepository):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self._conn = psycopg.connect(conn_string, autocommit=True)
        self._store = PostgresStore(conn=self._conn)
        self._store.setup()
```


---


## **🔧 Methods**


### 🔌 **store → BaseStore**

Get underlying PostgresStore for workflow compilation.

```python
@property
def store(self) -> BaseStore:
    return self._store
```

### 💾 **put() → None**

Store a value.

```python
def put(self, namespace: tuple, key: str, value: dict) -> None:
    self._store.put(namespace, key, value)
```

### 📥 **get() → dict**

Retrieve a value.

```python
def get(self, namespace: tuple, key: str) -> Optional[dict]:
    item = self._store.get(namespace, key)
    return item.value if item else None
```

### 🔍 **search() → list[dict]**

Search values in namespace.

```python
def search(self, namespace: tuple, query: str = None, limit: int = 10) -> list[dict]:
    results = self._store.search(namespace, query=query, limit=limit)
    return [item.value for item in results]
```

### 🗑️ **delete() → None**

Delete a value.

```python
def delete(self, namespace: tuple, key: str) -> None:
    self._store.delete(namespace, key)
```


---


## **💡 Usage**

```python
from src.repositories.stores.postgres.main import PostgresStoreRepository

store_repo = PostgresStoreRepository(
    host="localhost",
    port=5432,
    database="erp_agent",
    user="postgres",
    password="postgres",
)

# Store conversation turn
store_repo.put(
    namespace=("users", "user-456", "conversations"),
    key="thread-123_20241227_143000_abc12345",
    value={
        "query": "หาลำโพง bluetooth",
        "response": "พบลำโพง 5 รายการ...",
        "thread_id": "thread-123",
        "timestamp": "2024-12-27T14:30:00",
    },
)

# Get specific item
item = store_repo.get(
    namespace=("users", "user-456", "conversations"),
    key="thread-123_20241227_143000_abc12345",
)

# Search all conversations for user
items = store_repo.search(
    namespace=("users", "user-456", "conversations"),
    limit=50,
)
```


---


## **🔗 Infrastructure**

| Component | Documentation |
|-----------|---------------|
| PostgresClient | [libs/database/sql/postgres.md](../../../../libs/database/sql/postgres.md) |
| Docker Postgres | [docker/postgres.md](../../../../infrastructure/docker/postgres.md) |
