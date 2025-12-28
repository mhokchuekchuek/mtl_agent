# Repositories

Domain-specific data access layer. Repositories abstract infrastructure from business logic.

## Overview

| Repository | Purpose | Location |
|------------|---------|----------|
| [Chatbots](chatbots.md) | Compile workflow + memory management | `src/repositories/chatbots/` |
| [Checkpointers](checkpointers.md) | Short-term memory (per-thread, TTL) | `src/repositories/checkpointers/` |
| [Stores](stores.md) | Long-term memory (cross-thread, permanent) | `src/repositories/stores/` |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Usecase Layer                           │
│  ChatbotService                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Repository Layer                          │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ ChatbotRepo     │  │ Checkpointer │  │ StoreRepo      │  │
│  │ (compile+invoke)│  │ (Redis)      │  │ (Postgres)     │  │
│  └─────────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Modules Layer                           │
│  Workflows (uncompiled) │ Agents │ Tools                     │
└─────────────────────────────────────────────────────────────┘
```

## Repository vs libs/

| Layer | Scope | Example |
|-------|-------|---------|
| `libs/` | Generic infrastructure (cross-project) | `RedisClient`, `PostgresClient` |
| `repositories/` | Domain-specific (project-specific) | `CustomerChatbotRepository`, `RedisCheckpointerRepository` |

## References

- [Code Architecture](../architecture/code.md)
- [Why Checkpointer + Store](../decisions/why_checkpointer_and_store.md)
