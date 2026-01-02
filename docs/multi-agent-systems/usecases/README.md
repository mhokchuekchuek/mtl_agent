# Usecases

Application business logic layer.

## Location

`src/usecases/`

## Overview

Usecases orchestrate repositories to implement business operations. They are thin wrappers that delegate to repositories.

## Available Usecases

| Usecase | Purpose | Location |
|---------|---------|----------|
| ChatbotService | Generic chatbot operations | `src/usecases/chatbot/` |

## ChatbotService

Generic service that works with any `BaseChatbotRepository` implementation.

```python
from src.usecases.chatbot.main import ChatbotService

class ChatbotService:
    def __init__(self, chatbot_repo: BaseChatbotRepository):
        self._repo = chatbot_repo

    def chat(self, query: str, thread_id: str, user_id: Optional[str] = None) -> dict:
        """Process a chat query."""
        return self._repo.invoke(query, thread_id, user_id)

    def get_history(self, thread_id: str) -> list[BaseMessage]:
        """Get conversation history."""
        return self._repo.get_history(thread_id)

    def clear_conversation(self, thread_id: str) -> None:
        """Clear conversation memory."""
        self._repo.clear_conversation(thread_id)
```

## Usage

```python
from src.dependencies.customer_chatbot import build_chatbot_service

# Build service with all dependencies wired
service = build_chatbot_service()

# Use service
result = service.chat(
    query="หาลำโพง bluetooth",
    thread_id="thread-123",
    user_id="user-456",
)
print(result["response"])

# Get history
messages = service.get_history("thread-123")

# Clear conversation
service.clear_conversation("thread-123")
```

## Architecture

```
┌─────────────────────────────────────────┐
│             ChatbotService              │
│  (Business logic orchestration)         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        BaseChatbotRepository            │
│  ├── CustomerChatbotRepository          │
│  └── (Future: SupportChatbotRepository) │
└─────────────────────────────────────────┘
```

## References

- [Repositories](../repositories/README.md) - Data access layer
- [Dependencies](../dependencies/README.md) - DI wiring
