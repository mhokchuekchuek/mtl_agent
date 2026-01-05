# **🖥️ Self-Hosted LLM with vLLM**

---

## **📋 Overview**

Deploy private LLM infrastructure using vLLM for inference on Kubernetes.

---

## **❓ Why Consider This**

### 🧠 **LLMs Are Getting Smarter**

- Smaller models achieve equal or better quality than older large models
- Cost per query decreases as model efficiency improves
- Self-hosting becomes more economical at scale

### ✅ **Benefits**

| Benefit | Description |
|---------|-------------|
| Data Privacy | Keep sensitive data on-premises |
| Cost Control | Fixed infrastructure cost vs per-token pricing |
| Customization | Fine-tune models for specific use cases |
| Latency | Lower latency without network hops |
| No Rate Limits | Scale based on your infrastructure |

---

## **☸️ Kubernetes Deployment Options**

### 1️⃣ **Single-Node: Deployment**

Standard Kubernetes Deployment for single GPU node. Best for models that fit in one GPU (7B-13B parameters with quantization).

- Native K8s, no extra operators needed
- Simple scaling with HPA
- Use `nvidia.com/gpu` resource limits

### 2️⃣ **Multi-Node: LeaderWorkerSet (LWS)**

Kubernetes SIG project for deploying pods as a group. The leader (index 0) coordinates workers for distributed inference.

![LeaderWorkerSet Concept](../../assets/diagrams/future_improvements/lws_concept.png)

- **Gang Scheduling**: All pods in a replica scheduled together (all-or-nothing)
- **Dual Templates**: Separate specs for leader and workers
- **Unique Indexing**: Each pod gets index 0 to n-1
- Used by NVIDIA NIM, llm-d, Amazon EKS for multi-node LLM serving

### 3️⃣ **Multi-Node: Ray (KubeRay)**

KubeRay operator brings Ray's distributed computing to Kubernetes. Used by OpenAI for ChatGPT training.

![Ray E2E LLM](../../assets/diagrams/future_improvements/ray_e2e_llm.png)

- **Ray Serve** (`ray.serve.llm`): Auto-scaling, load balancing, vLLM integration
- **3-Level Autoscaling**: Ray Serve replicas → KubeRay workers → Cluster Autoscaler
- Part of PyTorch Foundation (2025)

### **⚖️ Comparison**

| Option | Pros | Cons |
|--------|------|------|
| **Deployment** | Simple setup, native K8s | Single node only |
| **LeaderWorkerSet** | Multi-node, native K8s CRD | Less ecosystem tooling |
| **Ray** | Used by OpenAI/ChatGPT, auto-scaling, dashboard, PyTorch Foundation | Extra operator overhead |

---

## **🔗 LiteLLM Integration**

Connect to vLLM via LiteLLM proxy for unified API gateway with caching, rate limiting, and observability.

---

## **⚖️ Trade-offs**

| Pros | Cons |
|------|------|
| Fixed cost at scale | High upfront GPU cost |
| Data stays private | Requires DevOps expertise |
| No vendor lock-in | Maintenance overhead |
| Customizable | Need enough traffic to justify cost |

---

## **🤔 When to Self-Host vs API**

| Scenario | Recommendation |
|----------|----------------|
| Low traffic (<10K req/day) | ❌ Use API - idle GPUs are expensive |
| High traffic (>100K req/day) | ✅ Self-host - cost savings at scale |
| Variable traffic | ❌ Use API - pay per use |
| Predictable steady traffic | ✅ Self-host - optimize utilization |
| Strict data privacy | ✅ Self-host - data on-premises |

---

## **📚 See Also**

- [Caching Strategy](caching.md) - LiteLLM cache, LMCache

---

## **🔗 References**

- [vLLM Kubernetes Docs](https://docs.vllm.ai/en/stable/deployment/k8s/)
- [vLLM Production Stack](https://github.com/vllm-project/production-stack)
- [LeaderWorkerSet Docs](https://lws.sigs.k8s.io/docs/overview/)
- [LeaderWorkerSet for Multi-Node LLM](https://www.cecg.io/blog/multinode-llm-serving)
- [KubeRay vLLM Integration](https://docs.vllm.ai/en/latest/deployment/integrations/kuberay/)
- [Ray LLM End-to-End Example](https://docs.ray.io/en/latest/ray-overview/examples/entity-recognition-with-llms/README.html)
- [LiteLLM vLLM Integration](https://docs.litellm.ai/docs/providers/vllm)
