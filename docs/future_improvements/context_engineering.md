# **🧠 Context Engineering**

Techniques for managing LLM context windows effectively in the MTL Agent system.

<details>
<summary>📊 Context Engineering Strategies</summary>

![Context Engineering Strategies](../assets/diagrams/future_improvements/context_engineering.png)

</details>


---


## **📋 What is Context Engineering?**

Context engineering is the art of filling the context window with **just the right information** at each step of an agent's trajectory. Think of it like RAM management for LLMs.

> "Context engineering is becoming the most important skill an AI engineer can develop."
> — [LangChain Blog](https://blog.langchain.com/context-engineering-for-agents/)


---


## **🎯 The 4 Strategies**

| Strategy | Action | Goal |
|----------|--------|------|
| **Write** | Save context outside window | Persist for later use |
| **Select** | Pull relevant context in | Only what's needed |
| **Compress** | Reduce token count | Fit more in window |
| **Isolate** | Split across agents | Focused context per task |

---


## **1️⃣ Write Context**

Save information outside the context window for later retrieval.

| Problem | Solution |
|---------|----------|
| SQL results (1000+ rows) bloat context | Save to scratchpad, keep only summary in messages |
| Context grows with each tool call | Write large data externally, reference by key |

**Techniques**: Scratchpad tools (`write_scratch`, `read_scratch`), Long-term memory store


---


## **2️⃣ Select Context**

Pull only relevant information into the context window.

| Problem | Solution |
|---------|----------|
| All 100+ messages loaded | Semantic selection - embed and find relevant messages |
| Agent gets distracted by irrelevant history | Keep only top-k similar + recent messages |

**Techniques**: Embedding-based message selection, Tool selection with RAG


---


## **3️⃣ Compress Context**

Reduce token count while retaining essential information.

| Problem | Solution |
|---------|----------|
| Messages grow unbounded (50K+ tokens) | Auto-summarize old messages |
| Large tool outputs | Show sample + summary, save full data to scratchpad |

**Techniques**: LLM summarization, Tool output compression


---


## **4️⃣ Isolate Context**

Split context across agents to maintain focus.

| Problem | Solution |
|---------|----------|
| Single agent sees everything | Route to specialized agents with isolated tools |
| Context bleeding between tasks | State schema isolation per agent |

**Current Implementation**: Orchestrator routes to ChatHistoryAgent or InsightAgent (each with own tools)

**Enhancement**: Parallel agent execution with isolated state fields


---


## **⚠️ Context Pathologies to Avoid**

| Pathology | Description | Prevention |
|-----------|-------------|------------|
| **Poisoning** | Hallucinations stored in context | Validate tool outputs before saving |
| **Distraction** | Irrelevant info overwhelms agent | Use semantic selection |
| **Confusion** | Conflicting information | Timestamp and version context |
| **Clash** | Context contradicts system prompt | Review prompts for conflicts |

---


## **🔗 References**

- [Context Engineering Blog](https://blog.langchain.com/context-engineering-for-agents/)
- [The Rise of Context Engineering](https://blog.langchain.com/the-rise-of-context-engineering/)
- [Context Engineering GitHub](https://github.com/langchain-ai/context_engineering)
- [Filesystems for Context Engineering](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/)
- [State of AI Agents 2025](https://www.langchain.com/state-of-agent-engineering)
