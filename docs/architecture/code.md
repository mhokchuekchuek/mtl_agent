# Code Architecture

## Architecture Pattern

**Clean Architecture** with Repository Pattern and Dependency Injection.

| Pattern | Purpose |
|---------|---------|
| Clean Architecture | Layered separation of concerns |
| Repository Pattern | Abstract data access |
| Dependency Injection | Decouple components via `src/dependencies/` |
| Selector Pattern | Swap infrastructure providers easily |

## Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                             │
│  src/api/routes/          - HTTP endpoints                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Dependencies Layer                         │
│  src/dependencies/        - DI wiring (build_chatbot_service)│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Usecase Layer                           │
│  src/usecases/            - Business logic orchestration     │
│  ChatbotService           - Generic chatbot operations       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Repository Layer                          │
│  src/repositories/                                           │
│  ├── chatbots/            - Compile workflow + memory mgmt   │
│  ├── checkpointers/       - Short-term memory (Redis)        │
│  └── stores/              - Long-term memory (Postgres)      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Modules Layer                           │
│  src/modules/agents/      - AI agents (Translation, Product) │
│  src/modules/tools/       - LangChain tools (SQL, VectorDB)  │
│  src/modules/workflows/   - LangGraph workflows (uncompiled) │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  libs/database/           - SQL, Vector, KeyValue clients    │
│  libs/llm/                - LLM clients, prompts, observ.    │
│  libs/configs/            - Configuration management         │
└─────────────────────────────────────────────────────────────┘
```

## Layers

| Layer | Location | Responsibility |
|-------|----------|----------------|
| API | `src/api/` | HTTP endpoints, request/response |
| Dependencies | `src/dependencies/` | DI wiring, service initialization |
| Usecase | `src/usecases/` | Business logic orchestration |
| Repository | `src/repositories/` | Chatbots, checkpointers, stores |
| Modules | `src/modules/` | Agents, Tools, Workflows |
| Infrastructure | `libs/` | Generic clients, configs |

## Repository Layer

| Folder | Purpose |
|--------|---------|
| `chatbots/` | Compile workflow + manage memory (invoke, get_history) |
| `checkpointers/` | Short-term memory (Redis) - per thread, TTL-based |
| `stores/` | Long-term memory (Postgres) - cross thread, permanent |

## Modules Layer

| Folder | Purpose |
|--------|---------|
| `agents/` | AI agents (TranslationAgent, ProductAgent) |
| `tools/` | LangChain tools (SQLTool, ProductSearchTool) |
| `workflows/` | LangGraph workflows (uncompiled graph definitions) |

## Workflow vs Repository

| Component | Location | Responsibility |
|-----------|----------|----------------|
| Workflow | `src/modules/workflows/` | Define graph structure (nodes, edges) |
| ChatbotRepository | `src/repositories/chatbots/` | Compile graph with checkpointer + store |

Workflows define business logic but don't compile. Repositories handle memory management and compilation.

## libs/ vs repository/

| Layer | Scope | Reusability | Example |
|-------|-------|-------------|---------|
| `libs/` | Generic infrastructure | Cross-project | `SQLiteClient`, `QdrantClient`, `RedisClient` |
| `repository/` | Domain-specific | Project-specific | `CustomerChatbotRepository`, `RedisCheckpointerRepository` |
