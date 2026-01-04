# **🐘 PostgreSQL**

Database for LiteLLM proxy configuration and logging.


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
| Database | `litellm` |
| Credentials | postgres/postgres (change in production) |

> ⚠️ **Important:** Change default credentials in production environments.


---


## **💡 Purpose**

- LiteLLM proxy configuration storage
- LiteLLM logging and analytics
