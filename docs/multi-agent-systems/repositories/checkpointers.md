# Checkpointer Repositories

Short-term conversation memory with TTL-based expiration.

## Overview

Checkpointers store LangGraph state per thread. Used for:
- Conversation continuity within a session
- Message history for context
- State persistence between turns

## Architecture

<details>
<summary>View Checkpointer Architecture</summary>

![Checkpointer Architecture](../images/repositories/checkpointer.png)

</details>

## Base Interface

```python
class BaseCheckpointerRepository(ABC):
    @property
    @abstractmethod
    def checkpointer(self) -> BaseCheckpointSaver:
        """Get underlying checkpointer for workflow injection."""
        pass

    @abstractmethod
    def get_checkpoint(self, thread_id: str) -> Optional[CheckpointTuple]:
        """Get checkpoint for a thread."""
        pass

    @abstractmethod
    def delete_checkpoint(self, thread_id: str) -> None:
        """Delete checkpoint for a thread."""
        pass
```

## Implementations

### RedisCheckpointerRepository

Redis-based checkpointer with TTL support.

| Config | Default | Description |
|--------|---------|-------------|
| `ttl` | 3600 | Time-to-live in seconds (60 min) |
| `refresh_on_read` | true | Extend TTL on each read |

```python
from src.repositories.checkpointers.redis.main import RedisCheckpointerRepository

repo = RedisCheckpointerRepository(
    redis_client=redis_client,
    ttl=3600,
    refresh_on_read=True,
)

# Get checkpointer for workflow compilation
checkpointer = repo.checkpointer

# Get conversation state
checkpoint = repo.get_checkpoint("thread-123")
messages = checkpoint.checkpoint["channel_values"]["messages"]

# Clear conversation
repo.delete_checkpoint("thread-123")
```

## Files

```
src/repositories/checkpointers/
├── __init__.py
├── base.py                 # BaseCheckpointerRepository
└── redis/
    ├── __init__.py
    └── main.py             # RedisCheckpointerRepository
```

## TTL Behavior

| Scenario | Behavior |
|----------|----------|
| User active | TTL refreshes on each message |
| User inactive 60 min | Checkpoint expires, cleared from Redis |
| Expired + new message | Fresh conversation starts |

## When to Use

| Use Case | Solution |
|----------|----------|
| Within session | Checkpointer (automatic) |
| Resume after TTL | Load from Store (manual) |
| Audit/Compliance | Store (permanent) |

## References

- [Stores](stores.md) - Long-term memory
- [Why Checkpointer + Store](../decisions/why_checkpointer_and_store.md)
- [Redis Docker](../docker/redis.md)
