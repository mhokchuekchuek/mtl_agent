# **⚙️ shared.yaml**

Common infrastructure settings inherited by all chatbots.


---


## **📍 Location**

[`configs/agents/shared.yaml`](../../../configs/agents/shared.yaml)


---


## **📋 Sections**


### 🤖 **llm**

LLM provider configuration via LiteLLM proxy.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| proxy_url | string | `@format {env[LITELLM_PROXY_URL]}` | LiteLLM proxy endpoint |
| api_key | string | `@format {env[LITELLM_MASTER_KEY]}` | LiteLLM master key |
| default_model | string | `gpt-4o-mini` | Default model |
| temperature | float | `0.7` | Default temperature |
| max_tokens | int | `2000` | Default max tokens |


### 📊 **observability**

Langfuse observability configuration.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| provider | string | `langfuse` | Provider name |
| host | string | `@format {env[LANGFUSE_BASE_URL]}` | Langfuse host URL |
| public_key | string | `@format {env[LANGFUSE_PUBLIC_KEY]}` | Langfuse public key |
| secret_key | string | `@format {env[LANGFUSE_SECRET_KEY]}` | Langfuse secret key |


### 🔴 **checkpointer**

Redis checkpointer for short-term memory.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| provider | string | `redis` | Provider name |
| host | string | `@format {env[REDIS_HOST]}` | Redis host |
| port | int | `@format {env[REDIS_PORT]}` | Redis port |
| ttl | int | `60` | TTL in minutes |
| refresh_on_read | bool | `true` | Refresh TTL on read |


### 🔍 **vectordb**

Qdrant vector database configuration.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| provider | string | `qdrant` | Provider name |
| host | string | `@format {env[QDRANT_HOST]}` | Qdrant host |
| port | int | `@format {env[QDRANT_PORT]}` | Qdrant port |


### 🗄️ **database**

SQLite ERP database configuration.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| provider | string | `sqlite` | Provider name |
| path | string | `@format {env[ERP_DATABASE_PATH]}` | Database file path |


### 🐘 **store**

Postgres store for long-term memory.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| provider | string | `postgres` | Provider name |
| host | string | `@format {env[POSTGRES_HOST]}` | Postgres host |
| port | int | `@format {env[POSTGRES_PORT]}` | Postgres port |
| database | string | `@format {env[POSTGRES_DB]}` | Database name |
| user | string | `@format {env[POSTGRES_USER]}` | Database user |
| password | string | `@format {env[POSTGRES_PASSWORD]}` | Database password |


---


## **🔗 Full Config**

See [`configs/agents/shared.yaml`](../../../configs/agents/shared.yaml) for complete configuration.
