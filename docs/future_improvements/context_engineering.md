# **🧠 Context Engineering**

Techniques for managing LLM context windows effectively in the MTL Agent system.

![Context Engineering Categories](../assets/diagrams/future_improvements/context_categories.png)

*Source: [LangChain Blog](https://blog.langchain.com/context-engineering-for-agents/)*


---


## **📋 What is Context Engineering?**

> "The delicate art and science of filling the context window with just the right information for the next step."
> — Andrej Karpathy

Context engineering treats the LLM's context window like **RAM in an operating system** - managing limited capacity to hold relevant information as agents perform tasks.

**Why it matters**: Long-running agent tasks accumulate tokens that can exceed context limits, increase costs/latency, and degrade performance. This is effectively the #1 job of engineers building AI agents.


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

![Write Context](../assets/diagrams/future_improvements/context_write.png)

**Examples**:
- **Scratchpads**: Agents take notes during tasks by writing to files or state objects
- **Memories**: Auto-generate long-term memories across sessions (like ChatGPT, Cursor)

**MTL Agent**:
- **Client Chatbot**: Save large SQL analytics results to scratchpad
- **Customer Chatbot**: Save order history to long-term memory (e.g., "what did I order yesterday?")


---


## **2️⃣ Select Context**

Pull only relevant information into the context window.

![Select Context](../assets/diagrams/future_improvements/context_select.png)

**Examples**:
- Pulling scratchpad notes via tool calls
- Using embeddings to retrieve task-relevant memories
- RAG for tool descriptions to fetch only appropriate tools
- Code agents selecting instructions from `.md` rules files

**MTL Agent**:
- **Client Chatbot**: Select relevant messages for analytics context
- **Customer Chatbot**: Select relevant past product discussions


---


## **3️⃣ Compress Context**

Reduce token count while retaining essential information.

![Compress Context](../assets/diagrams/future_improvements/context_compress.png)

**Examples**:
- **Summarization**: Claude Code applies "auto-compact" when context exceeds 95% capacity
- **Trimming**: Filter older messages or use trained pruners

**MTL Agent**:
- **Client Chatbot**: Summarize long analytics conversations
- **Customer Chatbot**: Summarize long shopping conversations


---


## **4️⃣ Isolate Context**

Split context across agents to maintain focus.

![Isolate Context](../assets/diagrams/future_improvements/context_isolate.png)

**Examples**:
- **Multi-agent systems**: Specialized agents each maintain separate context windows
- **Sandboxed environments**: Token-heavy objects (images, audio) remain external to LLM
- **State objects**: Expose only necessary information at each step

**MTL Agent**:
- **Client Chatbot**: Orchestrator routes to ChatHistoryAgent or InsightAgent (each with own tools)
- **Customer Chatbot**: Single ProductAgent with focused product/order context


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
