# **🌐 LiteLLM Proxy**

Unified LLM gateway with caching, logging, and routing.


---


## **📋 Container**

| Property | Value |
|----------|-------|
| Image | `ghcr.io/berriai/litellm:main-latest` |
| Container | `erp-agent-litellm-proxy` |
| Port | 4000 |
| Dashboard | http://localhost:4000/ui |


---


## **💡 Purpose**

- Centralized LLM gateway
- Response caching via Redis
- Request logging and analytics
- Model routing and fallbacks


---


## **⚙️ Configuration**

Config file: `configs/litellm/proxy_config.yaml`


### 🔑 **Environment Variables**

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key |
| `LITELLM_MASTER_KEY` | Master key for API authentication |
| `DATABASE_URL` | PostgreSQL URL for storing configs |

> ⚠️ **Important:** Never commit API keys to version control.


### ⚡ **LiteLLM Settings**

```yaml
litellm_settings:
  cache: false              # Redis caching (disabled by default)
  num_retries: 3            # Retry failed requests
  request_timeout: 600      # Timeout in seconds
  drop_params: true         # Drop unsupported params
```


### 🔀 **Router Settings**

```yaml
router_settings:
  routing_strategy: simple-shuffle  # Load balancing strategy

model_list:
- model_name: "*"           # Wildcard - accept all models
  litellm_params:
    model: "*"
```


### 📊 **Available Routing Strategies**

| Strategy | Description |
|----------|-------------|
| `simple-shuffle` | Random selection |
| `least-busy` | Route to least busy model |
| `latency-based-routing` | Route to fastest model |


---


## **🚀 Commands**

```bash
# Start LiteLLM
docker-compose up -d litellm-proxy

# View logs
docker-compose logs -f litellm-proxy

# Restart
docker-compose restart litellm-proxy
```


---


## **🧪 Testing**

```bash
# Health check
curl http://localhost:4000/health

# Test completion
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```


---


## **🔗 References**

- [LiteLLM Docs](https://docs.litellm.ai/docs/proxy/configs)
