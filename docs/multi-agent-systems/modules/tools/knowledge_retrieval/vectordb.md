# VectorDB Tools

Semantic search tools using vector embeddings stored in Qdrant.

## Location

`src/modules/tools/knowledge_retrieval/vectordb/`

## Tools

### ProductSearchTool

Semantic search for products using text queries.

**Location**: `src/modules/tools/knowledge_retrieval/vectordb/search.py`

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `vector_store` | BaseVectorStore | Vector store client |
| `llm_client` | BaseLLM | LLM client for embeddings |

**Input Schema**:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | str | required | Search query text |
| `top_k` | int | 10 | Number of results |

**Returns**: List of dicts with `product_id`, `score`, `metadata`

### SimilarProductsTool

Find products similar to a given product.

**Location**: `src/modules/tools/knowledge_retrieval/vectordb/similar.py`

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `vector_store` | BaseVectorStore | Vector store client |
| `llm_client` | BaseLLM | LLM client (for consistency) |

**Input Schema**:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `product_id` | int | required | Base product ID |
| `top_k` | int | 5 | Number of similar products |

**Returns**: List of dicts with `product_id`, `score`, `metadata`

## Usage

```python
from libs.database.vector.qdrant.main import VectorStoreClient
from libs.llm.client.litellm.main import LLMClient
from src.modules.tools.knowledge_retrieval.vectordb.search import ProductSearchTool
from src.modules.tools.knowledge_retrieval.vectordb.similar import SimilarProductsTool

# Initialize clients
vector_store = VectorStoreClient(
    host='localhost',
    port=6333,
    collection_name='products',
)
llm_client = LLMClient(
    proxy_url='http://localhost:4000',
    embedding_model='text-embedding-3-small',
    api_key='sk-1234',
)

# Create tools
search_tool = ProductSearchTool(
    vector_store=vector_store,
    llm_client=llm_client,
)
similar_tool = SimilarProductsTool(
    vector_store=vector_store,
    llm_client=llm_client,
)

# Direct usage
results = search_tool._run(query='wireless speaker', top_k=5)
similar = similar_tool._run(product_id=14, top_k=3)

# LangChain usage (for agents)
results = search_tool.run({'query': 'wireless speaker', 'top_k': 5})
similar = similar_tool.run({'product_id': 14, 'top_k': 3})
```

## Example Output

**Search for "wireless speaker"**:
```python
[
    {'product_id': 14, 'score': 0.5619, 'metadata': {...}},
    {'product_id': 6, 'score': 0.5294, 'metadata': {...}},
    {'product_id': 25, 'score': 0.4538, 'metadata': {...}},
]
```

**Similar to product 14**:
```python
[
    {'product_id': 25, 'score': 0.6698, 'metadata': {...}},
    {'product_id': 6, 'score': 0.6663, 'metadata': {...}},
    {'product_id': 69, 'score': 0.6602, 'metadata': {...}},
]
```
