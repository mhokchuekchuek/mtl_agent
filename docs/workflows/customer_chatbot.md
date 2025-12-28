# CustomerChatbotWorkflow

Fixed workflow for customer shopping assistant chatbot.

## Overview

Uses LangGraph with fixed flow:
1. Translate input to English
2. Process with ProductAgent (ReAct)
3. Translate response back to user's language

## Workflow

```
User Query
    │
    ▼
┌─────────────────┐
│ translate_input │  ← TranslationAgent (detect + translate to English)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  product_agent  │  ← ProductAgent (ReAct with tools)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│translate_output │  ← TranslationAgent (translate back to user language)
└─────────────────┘
    │
    ▼
Response
```

## Memory

| Type | Storage | Purpose |
|------|---------|---------|
| Short-term | Redis Checkpointer | Per-thread conversation state (TTL: 60 min) |
| Long-term | Postgres Store | Cross-thread backup (permanent) |

See [Why Checkpointer + Store](../decisions/why_checkpointer_and_store.md) for details.

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| CustomerChatbotWorkflow | Fixed Workflow (LangGraph) | Orchestrate translation + product agent |
| [TranslationAgent](../agents/README.md) | Simple Agent | Detect language, translate Thai ↔ English |
| [ProductAgent](../agents/products.md) | ReAct Agent | Handle product queries with tools |

## Tools

| Tool | Purpose |
|------|---------|
| [SQLTool](../tools/knowledge_retrieval/sql.md) | Natural language to SQL for stock, price, compare |
| [ProductSearchTool](../tools/knowledge_retrieval/vectordb.md) | Semantic product search |
| [SimilarProductsTool](../tools/knowledge_retrieval/vectordb.md) | Find similar products |

## LLM Clients

| Client | Use Case |
|--------|----------|
| litellm | Tools (`embed()`, `generate()`), TranslationAgent |
| langchain | ProductAgent (ReAct needs `ChatOpenAI`) |

## Usage

```python
from src.dependencies.customer_chatbot import build_chatbot_service

# Build service with all dependencies
service = build_chatbot_service()

# Chat with thread_id and user_id
result = service.chat(
    query="หาลำโพง bluetooth",
    thread_id="thread-123",
    user_id="user-456",
)
print(result["response"])
```

## State

| Key | Type | Description |
|-----|------|-------------|
| query | str | User's raw query |
| user_language | str | Detected language ("th" / "en") |
| translated_query | str | Query in English |
| response | str | Final response in user's language |

## Features

- **Short-term Memory**: Redis checkpointer with TTL
- **Long-term Memory**: Postgres store (saves every turn)
- **Observability**: Langfuse tracing via callback handler
- **Multi-language**: Automatic translation TH ↔ EN

## Files

```
src/modules/workflows/customer_chatbot/
├── __init__.py
├── state.py      # ShoppingState
└── main.py       # CustomerChatbotWorkflow (uncompiled)

src/repositories/chatbots/customer/
├── __init__.py
└── main.py       # CustomerChatbotRepository (compiles + memory)
```

## References

| Topic | Description |
|-------|-------------|
| [Architecture](../architecture/README.md) | Code architecture and patterns |
| [Why ReAct](../decisions/why_react_agent.md) | Decision on using ReAct pattern |
| [Why Checkpointer + Store](../decisions/why_checkpointer_and_store.md) | Decision on memory architecture |
