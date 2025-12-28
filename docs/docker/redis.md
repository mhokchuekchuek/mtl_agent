# Redis

Caching layer for LiteLLM responses and session memory.

## Configuration

```yaml
redis:
  image: redis/redis-stack-server:latest
  ports:
    - "6379:6379"
```

## Details

| Property | Value |
|----------|-------|
| Image | `redis/redis-stack-server:latest` |
| Port | 6379 |
| Volume | `redis_data` |

## Purpose

- Caching for LiteLLM responses
- Session memory storage
