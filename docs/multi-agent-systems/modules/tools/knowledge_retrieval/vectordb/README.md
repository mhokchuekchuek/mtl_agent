# VectorDB Tools

Semantic search tools using vector embeddings stored in Qdrant.

## Location

`src/modules/tools/knowledge_retrieval/vectordb/`

## Architecture

```
src/modules/tools/knowledge_retrieval/vectordb/
├── search.py      # ProductSearchTool - text query search
└── similar.py     # SimilarProductsTool - product similarity
```

## Documentation

---

### search

| File | Description |
|------|-------------|
| [search.md](search.md) | Product search by text query |

### similar

| File | Description |
|------|-------------|
| [similar.md](similar.md) | Find similar products |
