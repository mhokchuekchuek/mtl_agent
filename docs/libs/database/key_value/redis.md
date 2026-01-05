# **🗄️ Redis Client**

Redis key-value store client.


---


## **📍 Location**

[`libs/database/key_value/redis/`](../../../../libs/database/key_value/redis/)


---


## **⚙️ Configuration**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | "localhost" | Redis host |
| `port` | int | 6379 | Redis port |
| `db` | int | 0 | Redis database number |
| `password` | str | None | Redis password |


---


## **💡 Usage**

```python
from libs.database.key_value.selector import KeyValueSelector

client = KeyValueSelector.create(
    provider="redis",
    host="localhost",
    port=6379,
)

# Basic operations
client.set("user:123", b'{"name": "John"}', ttl=3600)
data = client.get("user:123")
client.delete("user:123")
```


---


## **🔄 With LangGraph Checkpointer**

Used by `RedisCheckpointerRepository` for conversation memory:

```python
from libs.database.key_value.selector import KeyValueSelector
from src.repositories.checkpointers.redis.main import RedisCheckpointerRepository

redis_client = KeyValueSelector.create(
    provider="redis",
    host="localhost",
    port=6379,
)

checkpoint_repo = RedisCheckpointerRepository(
    redis_client=redis_client,
    ttl=3600,  # 60 min
    refresh_on_read=True,
)
```


---


## **🐳 Docker**

See [Docker Redis](../../../infrastructure/docker/redis.md) for container setup.


---


## **📋 Config Example**

```yaml
# configs/agents/shared.yaml
checkpointer:
  provider: redis
  host: localhost
  port: 6379
  ttl: 3600
  refresh_on_read: true
```
