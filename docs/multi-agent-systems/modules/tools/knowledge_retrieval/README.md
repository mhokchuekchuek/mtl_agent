# Knowledge Retrieval Tools

Tools for searching and retrieving information from various data sources.

## Location

`src/modules/tools/knowledge_retrieval/`

## Architecture

```
src/modules/tools/knowledge_retrieval/
├── sql/                 # Natural language to SQL
│   ├── base/           # Base class and validator
│   ├── client/         # Client chatbot tools
│   └── customer/       # Customer chatbot tools
└── vectordb/           # Semantic search
    ├── search.py       # Product search
    └── similar.py      # Similar products
```

## Documentation

---

### sql

| Folder | Description |
|--------|-------------|
| [sql/](sql/README.md) | Natural language to SQL queries |

### vectordb

| Folder | Description |
|--------|-------------|
| [vectordb/](vectordb/README.md) | Semantic search on vector embeddings |
