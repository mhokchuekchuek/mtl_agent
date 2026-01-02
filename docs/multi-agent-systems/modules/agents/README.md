# Agents

LLM-powered agents for complex reasoning and orchestration.

## Location

`src/modules/agents/`

## Architecture

```
src/modules/agents/
├── base.py              # BaseAgent abstract class
├── client/              # Client chatbot agents
│   ├── orchestrator.py  # Intent classification
│   ├── insight.py       # BI analytics
│   └── chat_history.py  # Chat lookup
├── products/            # Customer chatbot
│   └── main.py          # Product queries
└── translation/         # Shared
    └── main.py          # Thai ↔ English
```

## Documentation

---

### base

| File | Description |
|------|-------------|
| [base.md](base.md) | BaseAgent abstract class |

### client

| File | Description |
|------|-------------|
| [orchestrator.md](client/orchestrator.md) | Intent classification and routing |
| [insight.md](client/insight.md) | BI analytics and visualization |
| [chat_history.md](client/chat_history.md) | Customer chat history lookup |

### products

| File | Description |
|------|-------------|
| [main.md](products/main.md) | Product queries, orders, recommendations |

### translation

| File | Description |
|------|-------------|
| [main.md](translation/main.md) | Thai ↔ English translation |
