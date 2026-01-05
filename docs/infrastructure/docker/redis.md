# **🔴 Redis**

Key-value store for LangGraph Checkpointer (short-term memory) and LiteLLM caching.


---


## **⚙️ Configuration**

```yaml
redis:
  image: redis/redis-stack-server:latest
  ports:
    - "6379:6379"
```


---


## **📋 Details**

| Property | Value |
|----------|-------|
| Image | `redis/redis-stack-server:latest` |
| Port | 6379 |
| Volume | `redis_data` |


---


## **💡 Purpose**

- LangGraph Checkpointer for short-term memory (conversation state)
- Caching for LiteLLM responses


---


## **🔗 Related**

- [Redis Client](../../libs/database/key_value/redis.md)
- [Why Checkpointer + Store](../../decisions/why_checkpointer_and_store.md)
