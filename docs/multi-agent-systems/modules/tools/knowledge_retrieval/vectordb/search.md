# Product Search Tool

Semantic search for products using natural language.

## Location

`src/modules/tools/knowledge_retrieval/vectordb/search.py`

## Overview

Search for products using semantic similarity. Useful when customer describes what they want in natural language instead of exact product names.

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | str | required | Search query text (e.g., "wireless headphones") |
| `top_k` | int | 10 | Maximum number of results |
| `similarity_threshold` | float | 0.5 | Minimum similarity score (0-1) |

## Flow Diagram

```mermaid
flowchart TD
    START[Customer search query] --> EMBED[1. Generate embedding]
    
    EMBED --> |query text| LLM[LLM Embedding API]
    LLM --> |vector 1536 dims| VECTOR[Query Vector]
    
    VECTOR --> SEARCH[2. Search Qdrant]
    SEARCH --> |cosine similarity| QDRANT[(Qdrant Vector DB)]
    
    QDRANT --> |top_k results| RAW[Raw Results]
    
    RAW --> FILTER[3. Filter by threshold]
    FILTER --> |score >= 0.5| FILTERED[Filtered Results]
    
    FILTERED --> FORMAT[4. Format response]
    FORMAT --> RESULTS[Return product matches]
```

## How It Works

### Step 1: Text to Vector

Customer's query is converted to a vector embedding:

```
"wireless headphones" → [0.023, -0.156, 0.089, ...] (1536 dimensions)
```

### Step 2: Vector Search

The query vector is compared against all product vectors in Qdrant:

```mermaid
flowchart LR
    subgraph Qdrant
        P1[Product 1 vector]
        P2[Product 2 vector]
        P3[Product 3 vector]
        PN[Product N vector]
    end
    
    Q[Query vector] --> |cosine similarity| P1
    Q --> |cosine similarity| P2
    Q --> |cosine similarity| P3
    Q --> |cosine similarity| PN
```

### Step 3: Similarity Scoring

| Score | Meaning |
|-------|---------|
| 1.0 | Exact match |
| 0.7+ | Very relevant |
| 0.5+ | Somewhat relevant |
| < 0.5 | Filtered out |

### Step 4: Return Results

Results sorted by similarity score (highest first).

## Database Access

### Qdrant Vector Database

| Collection | Content | Purpose |
|------------|---------|---------|
| products | Product embeddings | Semantic search |

### What's Stored in Qdrant

Each product has:

| Field | Type | Example |
|-------|------|---------|
| vector | float[1536] | Embedding of combined product text |
| product_id | int | 10 |
| product_name | string | "Gaming Chair" |
| source_file | string | "10_gaming_chair.pdf" |
| text | string | Combined text (name + description + specs + features) |

> **Note:** Fields like `category`, `price`, and full `description` are stored in the SQL database, not in Qdrant.

**Database Changes**: None (read-only search)

## Example

### Input
```
Customer: I'm looking for wireless headphones
```

### Step-by-Step

1. **Generate embedding** for "wireless headphones"
2. **Search Qdrant** for similar product vectors
3. **Filter** results with score >= 0.5
4. **Return** matching products

### Response
```python
{
    "query": "wireless headphones",
    "results": [
        {
            "product_id": 5,
            "score": 0.82,
            "metadata": {
                "product_name": "Wireless Bluetooth Headphones",
                "category": "Electronics",
                "price": 149.99
            }
        },
        {
            "product_id": 8,
            "score": 0.76,
            "metadata": {
                "product_name": "Noise Cancelling Headphones",
                "category": "Electronics",
                "price": 299.99
            }
        }
    ]
}
```

## When to Use

| Use Case | Tool |
|----------|------|
| "I want something for gaming" | ✅ ProductSearchTool (semantic) |
| "Show me product ID 10" | ❌ Use SQL tool (exact) |
| "wireless speaker under $100" | ✅ Search + SQL filter |

## Comparison with SQL

| Aspect | VectorDB Search | SQL Query |
|--------|-----------------|-----------|
| Query type | Natural language | Exact match |
| "gaming accessories" | ✅ Finds related products | ❌ Needs exact category |
| "something for work from home" | ✅ Understands intent | ❌ Cannot interpret |
| Speed | Fast (pre-indexed) | Fast |

## Error Cases

| Error | Cause | Response |
|-------|-------|----------|
| Empty results | No products match query | `{"results": []}` |
| Embedding failed | LLM API error | `{"error": "..."}` |

## References

- [ProductSearchTool](../../../../../../src/modules/tools/knowledge_retrieval/vectordb/search.py)
