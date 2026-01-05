# **👤 customer_chatbot.yaml**

Configuration for customer shopping assistant.


---


## **📍 Location**

[`configs/agents/customer_chatbot.yaml`](../../../configs/agents/customer_chatbot.yaml)


---


## **🤖 Agents**


### 🌐 **translation**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `agents_customer_translation` | Langfuse prompt name |
| temperature | `0.3` | Low for consistent translation |
| max_tokens | `8192` | Max output tokens |


### 🛒 **products**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `agents_customer_product_agent` | Langfuse prompt name |
| temperature | `0.7` | Moderate for natural responses |
| max_iterations | `5` | ReAct max iterations |


#### 🔧 **Tools: product_sql**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_customer_product_sql` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic SQL |
| allow_write | `false` | Read-only |
| allowed_tables | `Products, Inventory, Warehouses` | Accessible tables |


#### 🔧 **Tools: order_sql**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_customer_order_sql` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic SQL |
| allow_write | `false` | Read-only |
| allowed_tables | `Orders, OrderDetails, Products` | Accessible tables |


#### 🔧 **Tools: place_order_sql**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_customer_place_order_sql` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic SQL |
| allow_write | `true` | Write enabled |
| allowed_tables | `Orders, OrderDetails, Inventory, Products` | Accessible tables |


#### 🔧 **Tools: cancel_order_sql**

| Key | Value | Description |
|-----|-------|-------------|
| model | `gpt-4o-mini` | LLM model |
| prompt_name | `tools_customer_cancel_order_sql` | Langfuse prompt name |
| temperature | `0` | Zero for deterministic SQL |
| allow_write | `true` | Write enabled |
| allowed_tables | `Orders, OrderDetails, Inventory` | Accessible tables |


#### 🔧 **Tools: product_search**

| Key | Value | Description |
|-----|-------|-------------|
| embedding_model | `text-embedding-3-small` | OpenAI embedding model |
| top_k | `10` | Max results returned |
| similarity_threshold | `0.5` | Min similarity score |


#### 🔧 **Tools: similar_products**

| Key | Value | Description |
|-----|-------|-------------|
| embedding_model | `text-embedding-3-small` | OpenAI embedding model |
| top_k | `5` | Max similar products |


---


## **🔍 VectorDB**

| Key | Value | Description |
|-----|-------|-------------|
| collection_name | `products` | Qdrant collection name |


---


## **🔗 Full Config**

See [`configs/agents/customer_chatbot.yaml`](../../../configs/agents/customer_chatbot.yaml) for complete configuration.
