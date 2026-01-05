# **🔮 Future Improvements**

Potential enhancements for production readiness and better performance.


---


## **🤖 Agent Architecture**

| Topic | Description |
|-------|-------------|
| [Deep Agents Integration](deep_agents_integration.md) | LangChain Deep Agents with planning, subagents, and scratch space |
| [Context Engineering](context_engineering.md) | 4 strategies: Write, Select, Compress, Isolate for context window management |


---


## **🔧 Infrastructure**

| Topic | Description |
|-------|-------------|
| [Caching Strategy](infrastructure/caching.md) | LiteLLM (LLM Response Cache), LMCache (KV Cache) |
| [Self-Hosted LLM](infrastructure/self_hosted_llm.md) | vLLM + Kubernetes deployment |


---


## **💬 Chat History Management**

Improvements for saving conversation data from Redis checkpointer (short-term) to Postgres store (long-term).

| Topic | Description |
|-------|-------------|
| [Async Store Writes](chat_history/async_store_writes.md) | Queue or scheduled job for async Postgres writes |


---


## **📥 Data Ingestion Pipeline**

Improvements for PDF ingestion pipeline to VectorDB (product catalog).

| Topic | Description |
|-------|-------------|
| [Workflow Orchestrator](ingestion/workflow_orchestrator.md) | Use Airflow/Flyte for scalable ingestion |
| [Search Algorithms](ingestion/search_algorithms.md) | Hybrid search with dense + sparse vectors |
| [Embedding Models](ingestion/embedding_models.md) | Better retrieval accuracy models |
| [Structured Payload](ingestion/structured_payload.md) | Store fields separately for filtering |
