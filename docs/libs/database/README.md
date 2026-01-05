# **🗄️ Database Module**

Database utilities and integrations.


---


## **📍 Location**

[`libs/database/`](../../../libs/database/)


---


## **📦 Submodules**

| | | |
|:---:|:---:|:---:|
| [🔷 **SQL**](sql/README.md)<br/>SQL database clients | [🔮 **Vector**](vector/README.md)<br/>Vector database clients | [🔴 **Key-Value**](key_value/README.md)<br/>Key-value store clients |


---


## **🏗️ Architecture**

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
