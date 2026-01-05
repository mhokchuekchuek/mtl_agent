# **🔍 Qdrant**

Vector database for product knowledge base semantic search.


---


## **⚙️ Configuration**

```yaml
qdrant:
  image: qdrant/qdrant:latest
  ports:
    - "6333:6333"  # REST API
    - "6334:6334"  # gRPC
```


---


## **📋 Details**

| Property | Value |
|----------|-------|
| Image | `qdrant/qdrant:latest` |
| REST Port | 6333 |
| gRPC Port | 6334 |
| Volume | `qdrant_storage` |
| Dashboard | http://localhost:6333/dashboard |


---


## **💡 Purpose**

- Store product PDF embeddings
- Semantic search for RAG agent


---


## **🔗 Related**

- [Qdrant Schema](../databases/qdrant.md)
- [Qdrant Client](../../libs/database/vector/qdrant.md)
