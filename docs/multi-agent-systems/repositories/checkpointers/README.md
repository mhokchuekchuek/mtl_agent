# Checkpointer Repositories

Short-term conversation memory with TTL-based expiration.

## Location

`src/repositories/checkpointers/`

## Overview

Checkpointers store LangGraph state per thread. Used for:
- Conversation continuity within a session
- Message history for context
- State persistence between turns

## Code Flow

```mermaid
flowchart LR
    1[1. ChatbotRepo requests checkpoint] --> 2[2. CheckpointerRepo.get_checkpoint]
    2 --> 3[3. Redis lookup by thread_id]
    3 --> 4[4. Return messages + state]
    4 --> 5[5. TTL refreshed on read]
```

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
        pass

    @abstractmethod
    def delete_checkpoint(self, thread_id: str) -> None:
        pass
```

## Implementations

| Repository | Storage | Documentation |
|------------|---------|---------------|
| RedisCheckpointerRepository | Redis | [redis/main.md](redis/main.md) |
| MemoryCheckpointerRepository | In-memory | For testing |

## TTL Behavior

```mermaid
flowchart LR
    A[User sends message] --> B{Checkpoint exists?}
    B --> |Yes| C[Load + refresh TTL]
    B --> |No| D[Create new]
    C --> E[Process message]
    D --> E
    E --> F[Save checkpoint]
    F --> G[TTL: 60 min]
```

| Scenario | Behavior |
|----------|----------|
| User active | TTL refreshes on each message |
| User inactive 60 min | Checkpoint expires, cleared from Redis |
| Expired + new message | Fresh conversation starts |
