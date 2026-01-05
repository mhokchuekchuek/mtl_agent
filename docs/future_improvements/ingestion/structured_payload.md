# **📦 Structured Payload**


---


## **📋 Current State**

All extracted data stored as flat `text` field for simplicity. See [Decision: Why Flat Text Payload](../../decisions/why_flat_text_payload.md).

```json
{
  "product_id": 10,
  "product_name": "Smartphone Tripod",
  "source_file": "10_smartphone_tripod.pdf",
  "text": "Smartphone Tripod... category: Mobile & Tablets, weight: 0.5 kg..."
}
```


---


## **🔧 Improvement**

Store extracted fields separately for filtering:

```json
{
  "product_id": 10,
  "product_name": "Smartphone Tripod",
  "source_file": "10_smartphone_tripod.pdf",
  "text": "Smartphone Tripod Capture stunning photos...",
  "category": "Mobile & Tablets",
  "product_type": "Mobile Accessories",
  "weight": 0.5,
  "color": "black"
}
```


---


## **⚠️ Challenge**

Requires extra LLM call to extract filters from user query:

![Filter Flow](../../assets/diagrams/future_improvements/structured_payload_filter_flow.png)


---


## **✅ Benefits**

| Benefit | Description |
|---------|-------------|
| Exact filtering | Query by category, price range, color |
| Faceted search | Show counts per category |
| Hybrid search | Filter first, then semantic search |


---


## **📅 Implementation Steps**

1. Add filter extraction prompt (query → JSON filters)
2. Update extractor to return structured dict
3. Update pipeline to store fields separately
4. Add filter builder in retrieval layer
5. Keep `text` field for semantic search


---


## **❓ When to Implement**

Consider if:
- Users need exact numeric filtering (price, weight)
- Need faceted navigation UI
- Semantic search alone gives poor precision
