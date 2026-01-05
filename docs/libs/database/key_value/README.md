# **🔴 Key-Value Database**

Key-value store clients for caching and session management.


---


## **📍 Location**

[`libs/database/key_value/`](../../../../libs/database/key_value/)


---


## **📦 Providers**

| | |
|:---:|:---:|
| [🔴 **Redis**](redis.md)<br/>Redis client wrapper | |


---


## **🔧 Interface**

```python
from libs.database.key_value.base import BaseKeyValueClient

class BaseKeyValueClient(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value by key."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value with optional TTL."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete key."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass

    @abstractmethod
    def get_client(self) -> Any:
        """Get underlying client instance."""
        pass
```


---


## **💡 Usage**

```python
from libs.database.key_value.selector import KeyValueSelector

# Create Redis client
client = KeyValueSelector.create(
    provider="redis",
    host="localhost",
    port=6379,
)

# Use client
client.set("key", b"value", ttl=3600)
value = client.get("key")
```


---


## **🎯 Use Cases**

| Use Case | Description |
|----------|-------------|
| LangGraph Checkpointer | Short-term conversation memory with TTL |
| Session Cache | User session data |
| Rate Limiting | Request counters |
