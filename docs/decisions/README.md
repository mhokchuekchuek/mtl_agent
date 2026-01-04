# **📝 Decisions**

Architecture and technology decisions for the project.

> 💡 **Tip:** Each decision document follows the ADR (Architecture Decision Record) format.


---


## **🌐 General**

| Decision | Description |
|----------|-------------|
| [Why LiteLLM](why_litellm.md) | Why use LiteLLM Proxy as centralized LLM gateway |
| [Why Langfuse](why_langfuse.md) | Why use Langfuse for observability, prompt management, and evaluation |
| [Why OpenAI Model](why_openai_model.md) | Why use OpenAI GPT-4o-mini |


---


## **⚙️ Ingestor**

| Decision | Description |
|----------|-------------|
| [Why PyPDF2 Parser](why_pypdf2_parser.md) | Why use PyPDF2 for PDF parsing |
| [Why LLM Extractor](why_llm_extractor.md) | Why use LLM for data extraction |
| [Why Flat Text Payload](why_flat_text_payload.md) | Why store data as flat text instead of structured fields |


---


## **🤖 Multi-Agent Systems**

| Decision | Description |
|----------|-------------|
| [Why ReAct and LangGraph](why_react_and_langgraph.md) | When to use ReAct agents vs LangGraph workflows |
| [Why Checkpointer + Store](why_checkpointer_and_store.md) | Why use both Redis Checkpointer and Postgres Store for memory |


---


## **🧪 Evaluation**

| Decision | Description |
|----------|-------------|
| [Why LLM-as-Judge](why_llm_as_judge.md) | Why use LLM-as-Judge pattern for evaluation |
