# LiteLLM Proxy

Unified LLM gateway with caching, logging, and routing.

## Configuration

```yaml
litellm-proxy:
  image: ghcr.io/berriai/litellm:main-latest
  ports:
    - "4000:4000"
```

## Details

| Property | Value |
|----------|-------|
| Image | `ghcr.io/berriai/litellm:main-latest` |
| Port | 4000 |
| Config | `configs/litellm/proxy_config.yaml` |
| Dashboard | http://localhost:4000/ui |

## Purpose

- Centralized LLM gateway
- Response caching via Redis
- Request logging and analytics
- Model routing and fallbacks
