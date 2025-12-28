# Agents

LLM-powered agents for complex reasoning and orchestration.

## Location

`src/modules/agents/`

## Base Class

All agents inherit from `BaseAgent`:

```python
from src.modules.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, ...):
        super().__init__(name="my_agent")
    
    def execute(self, state: dict) -> dict:
        # Process state and return updated state
        pass
```

## Available Agents

| Agent | Description | Documentation |
|-------|-------------|---------------|
| `translation` | Language ↔ English translation | [translation.md](translation.md) |
| `products` | Product search, recommend, compare, stock | [products.md](products.md) |
