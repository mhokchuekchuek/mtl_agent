# **👁️ LLM Observability**

LLM tracing and monitoring using the provider/selector pattern.


---


## **📍 Location**

[`libs/llm/observability/`](../../../../libs/llm/observability/)


---


## **📦 Providers**

| | |
|:---:|:---:|
| [📊 **Langfuse**](langfuse.md)<br/>Langfuse Cloud tracing | |


---


## **🔧 Classes**


### 🎯 **BaseObservability**

Abstract base class for observability clients.

**Location**: `libs/llm/observability/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `trace_generation(**kwargs)` | Trace LLM generation |
| `is_available()` | Check if backend is available |


### 🔀 **ObservabilitySelector**

Selector for observability providers.

**Location**: `libs/llm/observability/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create client instance |
| `list_providers()` | List available providers |
