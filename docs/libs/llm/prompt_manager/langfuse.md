# **📝 Langfuse Prompt Manager**

Langfuse client for centralized prompt management.


---


## **📍 Location**

[`libs/llm/prompt_manager/langfuse/main.py`](../../../../libs/llm/prompt_manager/langfuse/main.py)

---


## **📦 Class**

### `LangfusePromptManager`

Langfuse client for prompt storage and retrieval.


---


## **📋 Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `public_key` | str | `LANGFUSE_PUBLIC_KEY` env | Langfuse public key |
| `secret_key` | str | `LANGFUSE_SECRET_KEY` env | Langfuse secret key |
| `host` | str | `https://cloud.langfuse.com` | Langfuse host URL |

---


## **📋 Methods**


### `get_prompt(name, version, label) -> Any`

Retrieve prompt from Langfuse.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Prompt name |
| `version` | str | Prompt version (optional) |
| `label` | str | Prompt label (optional) |

### `upload_prompt(name, prompt, config, labels) -> Any`

Upload prompt to Langfuse.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Prompt name |
| `prompt` | str | Prompt template content |
| `config` | dict | Prompt configuration |
| `labels` | list | Labels to apply |

### `is_available() -> bool`

Check if Langfuse is available.

---


## **🚀 Usage**

```python
from libs.llm.prompt_manager.selector import PromptManagerSelector

# Create prompt manager
pm = PromptManagerSelector.create(
    provider="langfuse",
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="https://cloud.langfuse.com"
)

# Get prompt
prompt = pm.get_prompt("triage_classifier", version="latest", label="production")

# Upload prompt
pm.upload_prompt(
    name="triage_classifier",
    prompt="You are a support ticket classifier...",
    config={"model": "gpt-4o-mini", "temperature": 0.3},
    labels=["production", "v1"]
)
```

---


## **🔑 Environment Variables**

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```
