# Dependencies

Dependency injection wiring layer.

## Location

`src/dependencies/`

## Overview

Dependencies layer creates and wires all components together. Each file provides a `build_*_service()` function that returns a ready-to-use service.

## Available Dependencies

| File | Function | Returns |
|------|----------|---------|
| `customer_chatbot.py` | `build_chatbot_service()` | `ChatbotService` |

## build_chatbot_service()

Creates the customer chatbot service with all dependencies:

```python
from src.dependencies.customer_chatbot import build_chatbot_service

service = build_chatbot_service()
result = service.chat("หาลำโพง", "thread-123", "user-456")
```

## Dependency Graph

```
build_chatbot_service()
    │
    ├── ConfigSelector.create() → settings
    │
    ├── LLMClientSelector.create("litellm") → litellm_client
    ├── LLMClientSelector.create("langchain") → langchain_client
    ├── SQLSelector.create() → sql_client
    ├── VectorStoreSelector.create() → vector_store
    ├── ObservabilitySelector.create() → observability
    ├── PromptManagerSelector.create() → prompt_manager
    │
    ├── KeyValueSelector.create("redis") → redis_client
    │       │
    │       └── RedisCheckpointerRepository(redis_client)
    │
    ├── PostgresStoreRepository(...) → store_repo
    │
    ├── SQLTool(sql_client, litellm_client, ...)
    ├── ProductSearchTool(vector_store, litellm_client)
    ├── SimilarProductsTool(vector_store, litellm_client)
    │
    ├── TranslationAgent(litellm_client, ...)
    ├── ProductAgent(langchain_client, tools, ...)
    │
    ├── CustomerChatbotWorkflow(agents) → workflow (uncompiled)
    │
    ├── CustomerChatbotRepository(workflow, checkpoint_repo, store_repo)
    │
    └── ChatbotService(chatbot_repo) → RETURN
```

## Config Loading

Dependencies read from `configs/agents/`:

| Config File | Purpose |
|-------------|---------|
| `shared.yaml` | LLM, database, observability settings |
| `customer_chatbot.yaml` | Chatbot-specific settings |

## Adding New Chatbot

To add a new chatbot type (e.g., SupportChatbot):

1. Create workflow: `src/modules/workflows/support_chatbot/`
2. Create repository: `src/repositories/chatbots/support/`
3. Create dependency: `src/dependencies/support_chatbot.py`
4. Create config: `configs/agents/support_chatbot.yaml`

```python
# src/dependencies/support_chatbot.py
def build_support_service() -> ChatbotService:
    # ... wire dependencies
    return ChatbotService(support_repo)
```

## References

- [Usecases](../usecases/README.md) - Business logic layer
- [Repositories](../repositories/README.md) - Data access layer
- [Architecture](../architecture/code.md) - Overall architecture
