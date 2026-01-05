# **🐘 PostgreSQL**

Database for LangGraph Store (long-term memory) and LiteLLM proxy.


---


## **⚙️ Configuration**

```yaml
postgres:
  image: postgres:15-alpine
  ports:
    - "5432:5432"
```


---


## **📋 Details**

| Property | Value |
|----------|-------|
| Image | `postgres:15-alpine` |
| Port | 5432 |
| Volume | `postgres_data` |
| Credentials | postgres/postgres (change in production) |

> ⚠️ **Important:** Change default credentials in production environments.


---


## **📊 Databases**

| Database | Purpose |
|----------|---------|
| `erp_agent` | LangGraph Store (long-term memory) |
| `litellm` | LiteLLM proxy configuration and logging |


---


## **💡 Purpose**

- LangGraph Store for long-term memory (user preferences, facts)
- LiteLLM proxy configuration storage
- LiteLLM logging and analytics


---


## **🔗 Related**

- [PostgreSQL Schema](../databases/postgres.md)
