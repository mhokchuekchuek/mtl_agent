# **🔑 Environment Variables**

Configuration via environment variables.


---


## **⚙️ Setup**

```bash
cp .env.template .env
# Edit .env with your values
```


---


## **🐳 Docker vs Local Development**

| Variable | Local | Docker |
|----------|-------|--------|
| `QDRANT_HOST` | `localhost` | `qdrant` (override by docker-compose) |
| `REDIS_HOST` | `localhost` | `redis` (override by docker-compose) |
| `POSTGRES_HOST` | `localhost` | `postgres` (override by docker-compose) |
| `LITELLM_PROXY_URL` | `http://localhost:4000` | `http://litellm:4000` (override by docker-compose) |

> 📝 **Note:** `.env.template` uses `localhost` for local dev. docker-compose.yml overrides with service names.


---


## **📋 Variables**


### 🔐 **Required**

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |

> ⚠️ **Important:** Never commit API keys to version control.


### 🔍 **Database - Qdrant**

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_HOST` | `localhost` | Qdrant host |
| `QDRANT_PORT` | `6333` | Qdrant port |


### 🔴 **Database - Redis**

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |


### 🐘 **Database - PostgreSQL**

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_DB` | `erp_agent` | Database name (for long-term memory store) |
| `POSTGRES_USER` | `postgres` | PostgreSQL user |
| `POSTGRES_PASSWORD` | `postgres` | PostgreSQL password |
| `DATABASE_URL` | - | Full connection URL for LiteLLM |


### 🗄️ **Database - SQLite**

| Variable | Default | Description |
|----------|---------|-------------|
| `ERP_DATABASE_PATH` | `data/erp_database.db` | ERP SQLite database path |


### 🌐 **LiteLLM Proxy**

| Variable | Default | Description |
|----------|---------|-------------|
| `LITELLM_PROXY_URL` | `http://localhost:4000` | LiteLLM proxy URL |
| `LITELLM_MASTER_KEY` | `sk-1234` | LiteLLM master key |
| `LITELLM_SALT_KEY` | - | LiteLLM salt key |


### 📊 **Observability - Langfuse**

| Variable | Default | Description |
|----------|---------|-------------|
| `LANGFUSE_PUBLIC_KEY` | - | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | - | Langfuse secret key |
| `LANGFUSE_BASE_URL` | `https://cloud.langfuse.com` | Langfuse base URL |
