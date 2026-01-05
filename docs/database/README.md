# **🗄️ Databases**

Database systems used in the project.


---


## **📖 Documentation**

| | |
|:---:|:---:|
| [🗃️ **ERP Database**](erp-database.md)<br/>SQLite with products, orders, customers | [🐘 **PostgreSQL**](postgres.md)<br/>Long-term memory (LangGraph Store) |
| [🔍 **Qdrant**](qdrant.md)<br/>Vector database for semantic search | |


---


## **📊 Overview**

| Database | Type | Purpose | Location |
|----------|------|---------|----------|
| SQLite | Relational | ERP data (products, orders, customers) | `data/erp_database.db` |
| PostgreSQL | Relational | Long-term memory (LangGraph Store) | Docker container |
| Redis | Key-Value | Short-term memory (LangGraph Checkpointer) | Docker container |
| Qdrant | Vector | Product embeddings for semantic search | Docker container |

> 📝 **Note:** Redis is used as LangGraph Checkpointer. See [Redis Docker](../infrastructure/docker/redis.md) and [Redis Client](../libs/database/key_value/redis.md) for details.
