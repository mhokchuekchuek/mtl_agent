# Future Improvements

Potential enhancements for production readiness and better performance.

## Chat History Management

Improvements for saving conversation data from Redis checkpointer (short-term) to Postgres store (long-term).

| Topic | Description |
|-------|-------------|
| [Async Store Writes](async_store_writes.md) | Queue or scheduled job for async Postgres writes |

## Data Ingestion Pipeline

Improvements for PDF ingestion pipeline to VectorDB (product catalog).

| Topic | Description |
|-------|-------------|
| [Workflow Orchestrator](workflow_orchestrator.md) | Use Airflow/Flyte for scalable ingestion |
| [Search Algorithms](search_algorithms.md) | Hybrid search with dense + sparse vectors |
| [Embedding Models](embedding_models.md) | Better retrieval accuracy models |
| [Structured Payload](structured_payload.md) | Store fields separately for filtering |
