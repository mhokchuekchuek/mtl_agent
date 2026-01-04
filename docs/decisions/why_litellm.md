# **📝 Why LiteLLM**


---


## **🎯 Decision**

Use **LiteLLM Proxy** as the centralized LLM gateway.


---


## **📋 Context**

Multi-agent systems require:
- **Multiple LLM calls**: Different agents may use different models
- **Cost management**: Track token usage and costs
- **Reliability**: Retries, timeouts, fallbacks
- **Flexibility**: Switch models without code changes
- **Private LLM support**: Connect to self-hosted models


---


## **🔄 Options Considered**

| Feature | LiteLLM Proxy | Direct OpenAI SDK | LangChain |
|---------|---------------|-------------------|-----------|
| Multi-provider support | 100+ providers | OpenAI only | Multiple (via wrappers) |
| Centralized config | Yes (YAML) | No (code) | No (code) |
| Load balancing | Built-in | Manual | Manual |
| Retry/timeout | Configurable | Manual | Manual |
| Cost tracking | Built-in | Manual | Via callbacks |
| Caching | Multiple backends | Manual | Manual |
| Self-hosted LLM | vLLM, Ollama, TGI | Manual | Manual |
| API compatibility | OpenAI-compatible | Native | Custom |


---


## **💡 Decision Rationale**


### 1️⃣ **Centralized Configuration**

Single YAML file to configure all models, retries, and timeouts:

```yaml
litellm_settings:
  num_retries: 3
  request_timeout: 600
  drop_params: true

model_list:
  - model_name: "*"
    litellm_params:
      model: "*"
```


### 2️⃣ **OpenAI-Compatible API**

All agents use standard OpenAI SDK. LiteLLM proxies requests transparently:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:4000",  # LiteLLM proxy
    api_key=settings.litellm_master_key
)
```


### 3️⃣ **Self-Hosted / Private LLM Support**

Connect to vLLM or any OpenAI-compatible endpoint:

**vLLM:**
```yaml
model_list:
  - model_name: private-llama
    litellm_params:
      model: hosted_vllm/llama-3-70b
      api_base: https://your-vllm-server.com
```

**OpenAI-compatible API:**
```yaml
model_list:
  - model_name: custom-model
    litellm_params:
      model: openai/my-model
      api_base: https://your-private-api.com/v1
      api_key: your-key
```


### 4️⃣ **Easy Model Switching & Fallbacks**

Change models or add fallbacks without code changes:

```yaml
model_list:
  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
  - model_name: gpt-4o-mini
    litellm_params:
      model: anthropic/claude-3-haiku  # Fallback
```


### 5️⃣ **Multiple Caching Backends**

| Cache Type | Config `type` | Use Case |
|------------|---------------|----------|
| In-Memory | `local` | Single-process, development |
| Redis | `redis` | Distributed, multi-server |
| Redis Semantic | `redis-semantic` | Similarity-based caching |
| S3 Bucket | `s3` | Cloud persistent cache |
| GCS | `gcs` | Google Cloud Storage |
| Azure Blob | `azure-blob` | Azure storage |
| Qdrant Semantic | `qdrant-semantic` | Vector DB semantic caching |
| Disk | `disk` | Local disk storage |


### 6️⃣ **Built-in Reliability**

- **Retries**: Automatic retry on transient failures
- **Timeouts**: Configurable request timeouts
- **Fallbacks**: Route to backup models on failure
- **Load balancing**: Distribute requests across deployments


---


## **⚖️ Trade-offs**

| Pros | Cons |
|------|------|
| Centralized model management | Additional service to run |
| Provider-agnostic | Slight latency overhead |
| Easy to add self-hosted models | Learning curve for config |
| Built-in observability | Requires PostgreSQL for persistence |


---


## **⚙️ Configuration**

**Location**: `configs/litellm/proxy_config.yaml`

See [LiteLLM Docker Documentation](../infrastructure/docker/litellm.md) for configuration details.


---


## **🔗 References**

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM vLLM Integration](https://docs.litellm.ai/docs/providers/vllm)
- [LiteLLM Caching](https://docs.litellm.ai/docs/caching/all_caches)
- [OpenAI-Compatible Endpoints](https://docs.litellm.ai/docs/providers/openai_compatible)
