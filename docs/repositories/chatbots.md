# Chatbot Repositories

Compile workflows with memory and provide unified interface for chatbot operations.

## Overview

Chatbot repositories:
1. Receive uncompiled workflow from modules layer
2. Compile with checkpointer (short-term) + store (long-term)
3. Provide `invoke`, `get_history`, `clear_conversation` methods

## Architecture

```
ChatbotService
      │
      ▼
┌─────────────────────────────────────────┐
│       CustomerChatbotRepository         │
│  ┌───────────────────────────────────┐  │
│  │ workflow.build().compile(         │  │
│  │   checkpointer=redis,             │  │
│  │   store=postgres                  │  │
│  │ )                                 │  │
│  └───────────────────────────────────┘  │
│                                         │
│  invoke() → run graph + save to store   │
│  get_history() → from checkpointer      │
│  clear_conversation() → delete checkpoint│
└─────────────────────────────────────────┘
```

## Base Interface

```python
class BaseChatbotRepository(ABC):
    def __init__(
        self,
        checkpoint_repo: Optional[BaseCheckpointerRepository] = None,
        store_repo: Optional[BaseStoreRepository] = None,
    )

    @abstractmethod
    def invoke(self, query: str, thread_id: str, user_id: Optional[str] = None) -> dict

    def get_history(self, thread_id: str) -> list[BaseMessage]
    def clear_conversation(self, thread_id: str) -> None
    def _save_to_store(self, query, response, thread_id, user_id) -> None
```

## Implementations

### CustomerChatbotRepository

Shopping assistant chatbot for product queries.

| Feature | Description |
|---------|-------------|
| Workflow | CustomerChatbotWorkflow (translate → product agent → translate) |
| Memory | Redis checkpointer + Postgres store |
| Observability | Langfuse tracing |

```python
from src.repositories.chatbots.customer.main import CustomerChatbotRepository

repo = CustomerChatbotRepository(
    workflow=workflow,           # Uncompiled
    checkpoint_repo=checkpoint_repo,
    store_repo=store_repo,
    observability=observability,
)

result = repo.invoke(
    query="หาลำโพง bluetooth",
    thread_id="thread-123",
    user_id="user-456",
)
```

## Files

```
src/repositories/chatbots/
├── __init__.py
├── base.py                 # BaseChatbotRepository
└── customer/
    ├── __init__.py
    └── main.py             # CustomerChatbotRepository
```

## Why Repository Pattern?

**Same interface for multiple chatbot types:**

```python
# Current
CustomerChatbotRepository  # Shopping assistant

# Future
SupportChatbotRepository   # Support ticket chatbot
SalesChatbotRepository     # Sales qualification chatbot
```

All share the same interface: `invoke`, `get_history`, `clear_conversation`.

## References

- [Workflows](../workflows/README.md) - Uncompiled graph definitions
- [Checkpointers](checkpointers.md) - Short-term memory
- [Stores](stores.md) - Long-term memory
