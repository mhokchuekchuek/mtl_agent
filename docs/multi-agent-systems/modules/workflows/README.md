# Workflows

LangGraph workflows that orchestrate agents.

## Location

`src/modules/workflows/`

## Overview

Workflows define graph structure (nodes, edges) but do NOT compile. Compilation with checkpointer + store is handled by [ChatbotRepository](../repositories/chatbots.md).

## Available Workflows

| Workflow | Description | Documentation |
|----------|-------------|---------------|
| `customer_chatbot` | Shopping assistant chatbot | [customer_chatbot.md](customer_chatbot.md) |

## Base Class

```python
from src.modules.workflows.base import BaseWorkflow

class MyWorkflow(BaseWorkflow):
    def build(self) -> StateGraph:
        graph = StateGraph(MyState)
        # Add nodes and edges
        return graph  # NOT compiled
```
