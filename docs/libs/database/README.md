# Database Module

Database utilities and integrations.

## Location

`libs/database/`

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| SQL | SQL database clients | [sql/](sql/README.md) |
| Vector | Vector database clients | [vector/](vector/README.md) |
| Key-Value | Key-value store clients | [key_value/](key_value/README.md) |

## Architecture

```text
libs/database/
├── sql/              # SQL database clients
│   ├── base.py       # BaseSQLDatabase abstract class
│   ├── selector.py   # SQLSelector
│   └── sqlite/       # SQLite client
├── vector/           # Vector database clients
│   ├── base.py       # BaseVectorStore abstract class
│   ├── selector.py   # VectorStoreSelector
│   └── qdrant/       # Qdrant client
└── key_value/        # Key-value store clients
    ├── base.py       # BaseKeyValue abstract class
    ├── selector.py   # KeyValueSelector
    └── redis/        # Redis client
```
