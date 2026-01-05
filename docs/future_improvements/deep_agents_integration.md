# **🤖 Deep Agents Integration Plan**

Integrating [LangChain Deep Agents](https://github.com/langchain-ai/deepagents) patterns into the MTL Agent system.

![Deep Agents Architecture](../assets/diagrams/future_improvements/deep_agents_architecture.png)


---


## **🔄 Deep Agents vs Context Engineering**

| | Deep Agents | Context Engineering |
|---|-------------|---------------------|
| **Question** | "What should I do?" | "How do I manage memory?" |
| **Focus** | Planning & task delegation | Context window management |

**Example - Client Chatbot Query**: "Show top 5 customers with order trends and chart"

| Step | Deep Agents handles | Context Engineering handles |
|------|---------------------|----------------------------|
| 1 | Plan: break into 3 steps (query → analyze → visualize) | - |
| 2 | Spawn sql-analyst subagent | - |
| 3 | - | Save large SQL result to scratchpad (not in messages) |
| 4 | Spawn visualizer subagent | Select only relevant data from scratchpad |
| 5 | - | Compress old messages before next turn |

**Summary**: Deep Agents decides *what to do*, Context Engineering manages *memory while doing it*.

See [Context Engineering](context_engineering.md) for memory techniques.


---


## **❓ Why Deep Agents?**

Current system uses simple ReAct agents that struggle with:
- Multi-step analytics queries
- Context accumulation over long conversations
- Dynamic task delegation

Deep Agents solve these with: **Planning**, **Subagents**, and **Scratch Space**.


---


## **🏗️ Current vs. Deep Agents Architecture**

```
Current Architecture:
┌─────────────────────────────────────────────┐
│ Workflow (Fixed Graph)                      │
│  translate → orchestrator → agent → output  │
│                    ↓                        │
│              [fixed routing]                │
│            ↙            ↘                   │
│     ChatHistory      Insight                │
└─────────────────────────────────────────────┘

Deep Agents Architecture:
┌─────────────────────────────────────────────┐
│ Deep Agent (Dynamic)                        │
│  ┌─────────────────────────────────────┐    │
│  │ Planning: write_todos / read_todos  │    │
│  └─────────────────────────────────────┘    │
│                    ↓                        │
│  ┌─────────────────────────────────────┐    │
│  │ Execute: spawn subagents as needed  │    │
│  │  → SQLSubagent                      │    │
│  │  → VectorSearchSubagent             │    │
│  │  → VisualizationSubagent            │    │
│  └─────────────────────────────────────┘    │
│                    ↓                        │
│  ┌─────────────────────────────────────┐    │
│  │ Scratch Space: store intermediate   │    │
│  │ results, notes, context             │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## **🔗 References**

- [Deep Agents GitHub](https://github.com/langchain-ai/deepagents)
- [LangChain Blog: Deep Agents](https://blog.langchain.com/deep-agents/)
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
