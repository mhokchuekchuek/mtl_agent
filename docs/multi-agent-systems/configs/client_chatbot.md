# **💼 client_chatbot.yaml**

Configuration for internal BI chatbot.


---


## **📍 Location**

`configs/agents/client_chatbot.yaml`


---


## **🤖 Agents**


### 🌐 **translation**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `agents_client_translation` | Langfuse prompt name |
| temperature | `0.3` | Low for consistent translation |
| max_tokens | `8192` | Max output tokens |


### 🔀 **orchestrator**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `agents_client_orchestrator` | Langfuse prompt name |
| temperature | `0.3` | Low for consistent routing |


### 💬 **chat_history**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `agents_client_chat_history` | Langfuse prompt name |
| temperature | `0.7` | Moderate for natural responses |
| max_iterations | `5` | ReAct max iterations |
| recursion_limit | `25` | Graph recursion limit |


#### 🔧 **Tools: chat_history_sql**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_client_chat_history_sql` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic SQL |


### 📊 **insight**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `agents_client_insight` | Langfuse prompt name |
| temperature | `0.7` | Moderate for natural responses |
| max_iterations | `5` | ReAct max iterations |
| recursion_limit | `25` | Graph recursion limit |


#### 🔧 **Tools: analytics_sql**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_client_analytics_sql` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic SQL |
| max_tokens | `16384` | Large for complex queries |


#### 🔧 **Tools: visualization**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_client_visualization` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic chart code |
| max_tokens | `16384` | Large for Plotly code |


---


## **🔗 Full Config**

See [`configs/agents/client_chatbot.yaml`](../../../configs/agents/client_chatbot.yaml) for complete configuration.
