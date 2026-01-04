# **⚙️ Configs**

Evaluation configuration files.


---


## **📍 Location**

`configs/evaluation/`

---


## **📋 Files**

| File | Chatbot | Documentation |
|------|---------|---------------|
| `customer.yaml` | Customer chatbot | [customer.md](#customer-config) |
| `client.yaml` | Client chatbot | [client.md](#client-config) |

---


## **📋 Config Structure**

```yaml
{chatbot}_eval:
  api:
    endpoint: "http://localhost:8000/api/v1/chatbot/{chatbot}/chat"
    timeout: 180

  dataset_path: "data/eval_datasets/{chatbot}"
  results_path: "results/{chatbot}"
  pass_threshold: 0.7

  context: |
    Chatbot permissions and restrictions...

  sql_judge:
    enabled: true
    model: "gpt-4o"
    temperature: 0.0
    max_tokens: 16384
    prompt:
      name: "evaluation_judges_sql_judge"
      label: "latest"

  # ... other judges
```

---


## **⚙️ Settings**


### 🔗 **API**

| Setting | Description | Default |
|---------|-------------|---------|
| `endpoint` | Chatbot API URL | Required |
| `timeout` | Request timeout (seconds) | 180 |

### 📁 **Paths**

| Setting | Description |
|---------|-------------|
| `dataset_path` | Test cases location |
| `results_path` | Results output location |

### 📊 **Thresholds**

| Setting | Description | Default |
|---------|-------------|---------|
| `pass_threshold` | Minimum score to pass | 0.7 |

### 📝 **Context**

Chatbot-specific context passed to judges for evaluation:

```yaml
context: |
  This is a Customer Support Chatbot.
  - Can only view Products catalog
  - Cannot access other customers' data
```

---


## **⚖️ Judge Config**

Each judge has:

| Setting | Description |
|---------|-------------|
| `enabled` | Enable/disable judge |
| `model` | LLM model for evaluation |
| `temperature` | LLM temperature |
| `max_tokens` | Max response tokens |
| `prompt.name` | Langfuse prompt name |
| `prompt.label` | Langfuse prompt label |

---


## **👤 Customer Config**

| Judge | Enabled |
|-------|---------|
| SQL | Yes |
| Search | Yes |
| Response Quality | Yes |
| Visualization | No |

### 💼 **Client Config**

| Judge | Enabled |
|-------|---------|
| SQL | Yes |
| Search | No |
| Response Quality | Yes |
| Visualization | Yes |

---


## **📄 Full Configs**

- [`configs/evaluation/customer.yaml`](../../configs/evaluation/customer.yaml)
- [`configs/evaluation/client.yaml`](../../configs/evaluation/client.yaml)
