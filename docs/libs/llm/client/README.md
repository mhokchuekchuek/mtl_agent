# **🔗 LLM Client**

LLM client implementations using the provider/selector pattern.


---


## **📍 Location**

`libs/llm/client/`


---


## **📦 Providers**

| | |
|:---:|:---:|
| [🤖 **LiteLLM**](litellm.md)<br/>HTTP-based LiteLLM proxy client | [🔗 **LangChain**](langchain.md)<br/>LangChain ChatOpenAI wrapper |


---


## **🔧 Classes**


### 🎯 **BaseLLM**

Abstract base class for LLM clients.

**Location**: `libs/llm/client/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `generate(prompt, system_prompt, **kwargs)` | Generate text completion |
| `embed(texts, **kwargs)` | Generate embeddings |


### 🔀 **LLMClientSelector**

Selector for LLM client providers.

**Location**: `libs/llm/client/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create client instance |
| `list_providers()` | List available providers |
