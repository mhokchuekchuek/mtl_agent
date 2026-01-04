# Self-Hosted LLM with vLLM

## Overview

Deploy private LLM infrastructure using vLLM for inference on Kubernetes.

## Why Consider This

### LLMs Are Getting Smarter

- Future models require fewer tokens to produce better results
- Cost per query decreases as model efficiency improves
- Self-hosting becomes more economical at scale

### Benefits

| Benefit | Description |
|---------|-------------|
| Data Privacy | Keep sensitive data on-premises |
| Cost Control | Fixed infrastructure cost vs per-token pricing |
| Customization | Fine-tune models for specific use cases |
| Latency | Lower latency without network hops |
| No Rate Limits | Scale based on your infrastructure |

## Kubernetes Deployment Options

### Single-Node: Deployment

Standard Kubernetes Deployment for single GPU node:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        resources:
          limits:
            nvidia.com/gpu: 1
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
```

### Multi-Node: LeaderWorkerSet (LWS)

For large models sharded across multiple nodes, use LeaderWorkerSet instead of Deployment or StatefulSet:

```yaml
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: vllm-multi-node
spec:
  replicas: 1
  leaderWorkerTemplate:
    size: 2  # 1 leader + 1 worker
    leaderTemplate:
      spec:
        containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          resources:
            limits:
              nvidia.com/gpu: 8
```

### Production: Helm Charts

vLLM Production Stack provides ready-to-use Helm charts:

```bash
helm repo add vllm https://vllm-project.github.io/production-stack
helm install vllm vllm/vllm-stack -f values.yaml
```

## LiteLLM Integration

Connect to vLLM via LiteLLM proxy:

```yaml
model_list:
  - model_name: llama-3-70b
    litellm_params:
      model: hosted_vllm/meta-llama/Llama-3-70B-Instruct
      api_base: http://vllm-service:8000
```

## Trade-offs

| Pros | Cons |
|------|------|
| Fixed cost at scale | High upfront GPU cost |
| Data stays private | Requires DevOps expertise |
| No vendor lock-in | Maintenance overhead |
| Customizable | Need enough traffic to justify cost |

## When to Self-Host vs API

| Scenario | Recommendation |
|----------|----------------|
| Low traffic (<10K req/day) | ❌ Use API - idle GPUs are expensive |
| High traffic (>100K req/day) | ✅ Self-host - cost savings at scale |
| Variable traffic | ❌ Use API - pay per use |
| Predictable steady traffic | ✅ Self-host - optimize utilization |
| Strict data privacy | ✅ Self-host - data on-premises |

## See Also

- [Caching Strategy](caching.md) - LMCache, LiteLLM caching, semantic cache

## References

- [vLLM Kubernetes Docs](https://docs.vllm.ai/en/stable/deployment/k8s/)
- [vLLM Production Stack](https://github.com/vllm-project/production-stack)
- [LeaderWorkerSet for Multi-Node LLM](https://www.cecg.io/blog/multinode-llm-serving)
- [LiteLLM vLLM Integration](https://docs.litellm.ai/docs/providers/vllm)
