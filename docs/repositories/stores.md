# Store Repositories

Long-term conversation memory with permanent storage.

## Overview

Stores persist conversation data permanently. Used for:
- Backup when checkpointer TTL expires
- Cross-thread data access
- Audit and compliance
- Analytics

## Architecture

```
ChatbotRepository._save_to_store()
      │
      ▼
┌─────────────────────────────────────────┐
│       PostgresStoreRepository           │
│  ┌───────────────────────────────────┐  │
│  │ PostgresStore(                    │  │
│  │   conn=psycopg.connect(...)       │  │
│  │ )                                 │  │
│  └───────────────────────────────────┘  │
│                                         │
│  put(namespace, key, value)             │
│  get(namespace, key) → Item             │
│  search(namespace) → list[Item]         │
└─────────────────────────────────────────┘
      │
      ▼
  PostgreSQL
```

## Base Interface

```python
class BaseStoreRepository(ABC):
    @property
    @abstractmethod
    def store(self) -> BaseStore:
        """Get underlying store for workflow injection."""
        pass

    @abstractmethod
    def put(self, namespace: tuple, key: str, value: dict) -> None:
        """Store a value."""
        pass

    @abstractmethod
    def get(self, namespace: tuple, key: str) -> Optional[Item]:
        """Get a value."""
        pass

    @abstractmethod
    def search(self, namespace: tuple) -> list[Item]:
        """Search values in namespace."""
        pass
```

## Implementations

### PostgresStoreRepository

PostgreSQL-based store using LangGraph's PostgresStore.

```python
from src.repositories.stores.postgres.main import PostgresStoreRepository

repo = PostgresStoreRepository(
    host="localhost",
    port=5432,
    database="erp_agent",
    user="postgres",
    password="postgres",
)

# Store conversation turn
repo.put(
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
item = repo.get(
    namespace=("users", "user-456", "conversations"),
    key="thread-123_20241227_143000_abc12345",
)

# Search all conversations for user
items = repo.search(namespace=("users", "user-456", "conversations"))
```

## Files

```
src/repositories/stores/
├── __init__.py
├── base.py                 # BaseStoreRepository
└── postgres/
    ├── __init__.py
    └── main.py             # PostgresStoreRepository
```

## Namespace Structure

Namespaces are hierarchical tuples (like folders):

```
("users", user_id, "conversations")
   │        │           │
   │        │           └── Data type
   │        └── User identifier
   └── Top-level category
```

Example keys:
```
thread-123_20241227_143000_abc12345
   │           │       │      │
   │           │       │      └── UUID (uniqueness)
   │           │       └── Time (HHMMSS)
   │           └── Date (YYYYMMDD)
   └── Thread ID
```

## Manual Save

LangGraph store does NOT auto-save. Must call `store.put()` manually:

```python
# In BaseChatbotRepository._save_to_store()
def _save_to_store(self, query, response, thread_id, user_id):
    if not self.store_repo or not user_id:
        return

    namespace = ("users", user_id, "conversations")
    key = f"{thread_id}_{timestamp}_{uuid}"

    self.store_repo.put(namespace, key, {
        "query": query,
        "response": response,
        "thread_id": thread_id,
        "timestamp": datetime.now().isoformat(),
    })
```

## When to Use

| Use Case | How |
|----------|-----|
| Resume old conversation | `search(namespace)` → get messages → inject to new thread |
| Audit log | `search(namespace)` → export to CSV |
| Analytics | Query PostgreSQL directly |

## References

- [Checkpointers](checkpointers.md) - Short-term memory
- [Why Checkpointer + Store](../decisions/why_checkpointer_and_store.md)
- [Postgres Docker](../docker/postgres.md)
