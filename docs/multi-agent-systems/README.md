# Multi-Agent Systems

Documentation for the MTL Agent multi-agent system architecture, mirroring the `src/` code structure.

## Overview

This system implements two chatbot workflows:
- **Client Chatbot**: Analytics, insights, and visualization for internal users
- **Customer Chatbot**: Product search, orders, and support for customers

## Architecture Layers

| Layer | Purpose | Documentation |
|-------|---------|---------------|
| Modules | Core business logic (agents, tools, workflows) | [modules/](modules/) |
| Repositories | Data access layer | [repositories/](repositories/README.md) |
| Usecases | Business orchestration | [usecases/](usecases/README.md) |
| Dependencies | Dependency injection | [dependencies/](dependencies/README.md) |
| API | REST API endpoints | [api/](api/README.md) |
| UI | Streamlit user interface | [ui/](ui/) |
| CLI | Command-line interface | [cli/](cli/README.md) |

## Modules

### Agents
LLM-powered agents that handle specific tasks.

| Agent | Purpose | Documentation |
|-------|---------|---------------|
| Client Orchestrator | Routes client requests | [agents/client/orchestrator.md](modules/agents/client/orchestrator.md) |
| Client Insight | Generates business insights | [agents/client/insight.md](modules/agents/client/insight.md) |
| Client Chat History | Manages conversation context | [agents/client/chat_history.md](modules/agents/client/chat_history.md) |
| Products | Product information agent | [agents/products/](modules/agents/products/products.md) |
| Translation | Language translation | [agents/translation/](modules/agents/translation/translation.md) |

### Tools
LangChain tools used by agents.

| Tool | Purpose | Documentation |
|------|---------|---------------|
| SQL (Base) | Base SQL query generation | [tools/knowledge_retrieval/sql.md](modules/tools/knowledge_retrieval/sql.md) |
| VectorDB | Semantic search | [tools/knowledge_retrieval/vectordb.md](modules/tools/knowledge_retrieval/vectordb.md) |
| Visualization | Chart generation | [tools/visualization/](modules/tools/visualization/README.md) |

### Workflows
LangGraph workflows that orchestrate agents.

| Workflow | Purpose | Documentation |
|----------|---------|---------------|
| Client Chatbot | Internal analytics workflow | [workflows/client_chatbot/](modules/workflows/client_chatbot/client_chatbot.md) |
| Customer Chatbot | Customer-facing workflow | [workflows/customer_chatbot/](modules/workflows/customer_chatbot/customer_chatbot.md) |

## Code Structure Mapping

```
src/                              docs/multi-agent-systems/
├── modules/                      ├── modules/
│   ├── agents/                   │   ├── agents/
│   │   ├── client/               │   │   ├── client/
│   │   ├── products/             │   │   ├── products/
│   │   └── translation/          │   │   └── translation/
│   ├── tools/                    │   ├── tools/
│   │   └── knowledge_retrieval/  │   │   └── knowledge_retrieval/
│   └── workflows/                │   └── workflows/
│       ├── client_chatbot/       │       ├── client_chatbot/
│       └── customer_chatbot/     │       └── customer_chatbot/
├── repositories/                 ├── repositories/
├── usecases/                     ├── usecases/
└── dependencies/                 └── dependencies/
```
