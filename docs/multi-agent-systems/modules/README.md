# Modules

Core building blocks for multi-agent systems.

## Location

`src/modules/`

## Overview

Modules are the main components that power the chatbot systems. They follow a layered architecture where workflows orchestrate agents, and agents use tools.

### Customer Chatbot Flow

```mermaid
flowchart TD
    subgraph Workflow
        W[CustomerChatbotWorkflow]
    end
    
    subgraph Agents
        A1[TranslationAgent]
        A2[ProductAgent]
    end
    
    subgraph Tools
        T1[SQL Tools]
        T2[VectorDB Tools]
    end
    
    W --> A1
    W --> A2
    A2 --> T1
    A2 --> T2
```

### Client Chatbot Flow

```mermaid
flowchart TD
    subgraph Workflow
        W[ClientChatbotWorkflow]
    end
    
    subgraph Agents
        A1[TranslationAgent]
        A2[OrchestratorAgent]
        A3[ChatHistoryAgent]
        A4[InsightAgent]
    end
    
    subgraph Tools
        T1[SQL Tools]
        T2[Visualization]
    end
    
    W --> A1
    W --> A2
    A2 --> |CHAT_HISTORY| A3
    A2 --> |INSIGHT| A4
    A3 --> T1
    A4 --> T1
    A4 --> T2
```

## Components

| Component | Purpose | Documentation |
|-----------|---------|---------------|
| **Workflows** | Graph orchestrators | [workflows/README.md](workflows/README.md) |
| **Agents** | LLM-powered decision makers | [agents/README.md](agents/README.md) |
| **Tools** | Domain logic executors | [tools/README.md](tools/README.md) |

## Workflows

Workflows orchestrate agents using LangGraph StateGraph.

| Workflow | Pattern | Purpose |
|----------|---------|---------|
| [ClientChatbotWorkflow](workflows/client_chatbot/main.md) | Conditional | Internal BI chatbot |
| [CustomerChatbotWorkflow](workflows/customer_chatbot/main.md) | Fixed | Shopping assistant |

## Agents

Agents are LLM-powered components that make decisions and execute tasks.

| Agent | Type | Used By | Purpose |
|-------|------|---------|---------|
| [TranslationAgent](agents/translation/main.md) | Simple | Both | Language detection and translation |
| [OrchestratorAgent](agents/client/orchestrator.md) | Simple | Client | Intent classification |
| [InsightAgent](agents/client/insight.md) | ReAct | Client | SQL analytics + visualization |
| [ChatHistoryAgent](agents/client/chat_history.md) | ReAct | Client | Customer chat lookup |
| [ProductAgent](agents/products/main.md) | ReAct | Customer | Product queries + orders |

## Tools

Tools are domain logic components that agents can invoke.

| Tool Category | Tools | Used By | Purpose |
|---------------|-------|---------|---------|
| [SQL](tools/knowledge_retrieval/sql/README.md) | Analytics, ChatHistory, Product, Order | Both | Database queries |
| [VectorDB](tools/knowledge_retrieval/vectordb/README.md) | Search, Similar | Customer | Semantic search |
| [Visualization](tools/visualization/README.md) | Chart generation | Client | Plotly charts |

## Design Decisions

| Decision | Description | Link |
|----------|-------------|------|
| ReAct & LangGraph | When to use ReAct agents vs LangGraph workflows | [why_react_and_langgraph.md](../../decisions/why_react_and_langgraph.md) |
| OpenAI Model | Model selection rationale | [why_openai_model.md](../../decisions/why_openai_model.md) |
| Langfuse | Observability choice | [why_langfuse.md](../../decisions/why_langfuse.md) |

## Future Improvements

| Improvement | Description | Link |
|-------------|-------------|------|
| Workflow Orchestrator | Dynamic agent routing | [workflow_orchestrator.md](../../future_improvements/workflow_orchestrator.md) |
| Embedding Models | Better semantic search | [embedding_models.md](../../future_improvements/embedding_models.md) |
| Search Algorithms | Hybrid search strategies | [search_algorithms.md](../../future_improvements/search_algorithms.md) |
| Structured Payload | Type-safe tool outputs | [structured_payload.md](../../future_improvements/structured_payload.md) |

## File Structure

```
src/modules/
├── workflows/
│   ├── base.py                    # BaseWorkflow abstract class
│   ├── client_chatbot/            # Client workflow
│   └── customer_chatbot/          # Customer workflow
├── agents/
│   ├── base.py                    # BaseAgent abstract class
│   ├── translation/main.py        # TranslationAgent
│   ├── products/main.py           # ProductAgent
│   └── client/
│       ├── orchestrator.py        # OrchestratorAgent
│       ├── insight.py             # CustomerInsightAgent
│       └── chat_history.py        # CustomerChatHistoryAgent
└── tools/
    ├── knowledge_retrieval/
    │   ├── sql/                   # SQL tools
    │   └── vectordb/              # VectorDB tools
    └── visualization/             # Chart tools
```
