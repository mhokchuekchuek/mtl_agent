# **🔍 Qdrant Database**

Qdrant vector database for semantic product search.


---


## **📍 Connection**

| Property | Value |
|----------|-------|
| Host | `localhost` |
| Port | `6333` |
| Protocol | HTTP REST API |


---


## **📊 Collections**

| Collection | Points | Vector Size | Distance |
|------------|--------|-------------|----------|
| products | 100 | 1536 | Cosine |


---


## **📋 Schema**


### 🛍️ **products**

Product embeddings for semantic search.

**Vector:**
| Property | Value |
|----------|-------|
| Size | 1536 (text-embedding-3-small) |
| Distance | Cosine |

**Payload:**
| Field | Type | Description |
|-------|------|-------------|
| product_id | INTEGER | Product ID from ERP database |
| product_name | TEXT | Name of the product |
| source_file | TEXT | Source PDF filename |
| text | TEXT | Combined description + attributes for search |


---


## **💡 Usage**

```python
from libs.database.vector.selector import VectorSelector

db = VectorSelector.create(
    provider="qdrant",
    host="localhost",
    port=6333,
    collection_name="products"
)

# Search products
results = db.search(
    query_vector=embeddings,
    limit=5
)
```


---


## **🔗 Related**

- [Docker Setup](../infrastructure/docker/qdrant.md)
- [Qdrant Client](../libs/database/vector/qdrant.md)
- [Product Search Tool](../../multi-agent-systems/modules/tools/knowledge_retrieval/vectordb/search.md)
- [Ingestor Pipeline](../../ingestor/README.md)
