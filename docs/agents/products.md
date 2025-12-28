# ProductAgent

ReAct agent for handling product-related queries.

## Overview

ProductAgent uses LangChain v1's `create_agent` to build a ReAct (Reasoning + Acting) agent that dynamically decides which tools to use based on the user's query.

## Architecture

```
ProductAgent
    │
    └── LLM decides which tool(s) to use:
        ├── ProductSearchTool  - semantic search by name/description
        ├── SimilarProductsTool - find similar products
        └── SQLTool - stock, price, compare queries
```

## Capabilities

| Use Case | Example Query | Tools Used |
|----------|---------------|------------|
| Search | "หาลำโพง bluetooth" | ProductSearchTool |
| Recommend | "แนะนำสินค้าคล้ายนี้" | SimilarProductsTool |
| Compare | "เปรียบเทียบ A กับ B" | SQLTool |
| Stock/Price | "มีสต็อกไหม" | SQLTool |
| Complex | "หาลำโพงแล้วเช็คสต็อก" | Multiple tools |

## Usage

```python
from libs.llm.client.selector import LLMClientSelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from src.modules.agents.products.main import ProductAgent
from src.modules.tools.knowledge_retrieval.vectordb.search import ProductSearchTool
from src.modules.tools.knowledge_retrieval.vectordb.similar import SimilarProductsTool
from src.modules.tools.knowledge_retrieval.sql.main import SQLTool

# Initialize LLM client
langchain_client = LLMClientSelector.create(
    provider="langchain",
    proxy_url="http://litellm-proxy:4000",
    api_key="sk-1234",
)
llm = langchain_client.get_client(model="gpt-4o-mini")

# Initialize prompt manager
prompt_manager = PromptManagerSelector.create(provider="langfuse")

# Initialize tools
product_search = ProductSearchTool(vectordb_client)
similar_products = SimilarProductsTool(vectordb_client)
sql_tool = SQLTool(db_connection)

# Create agent
agent = ProductAgent(
    llm=llm,
    prompt_manager=prompt_manager,
    tools=[product_search, similar_products, sql_tool],
)

# Execute query
state = {"query": "หาลำโพง bluetooth ราคาไม่เกิน 2000"}
result = agent.execute(state)
print(result["response"])
```

## Interface

```python
class ProductAgent(BaseAgent):
    def __init__(
        self,
        llm: ChatOpenAI,
        prompt_manager: BasePromptManager,
        tools: list[BaseTool],
        prompt_name: str = "product_agent",
    )

    def execute(self, state: dict) -> dict
```

### Input State

| Key | Type | Description |
|-----|------|-------------|
| query | str | User's product query |

### Output State

| Key | Type | Description |
|-----|------|-------------|
| response | str | Agent's response |

## Prompt

The system prompt is loaded from Langfuse prompt manager using the `product_agent` prompt name.

Location: `prompts/customer_chatbot/product_agent.prompt`

## Dependencies

- `langchain.agents.create_agent` - LangChain v1 agent builder
- `langchain_openai.ChatOpenAI` - LLM client
- `libs.llm.prompt_manager.base.BasePromptManager` - Prompt management
- `src.modules.agents.base.BaseAgent` - Base agent class

## Decisions

- [Why ReAct Agent](../decisions/why_react_agent.md) - Why we chose ReAct pattern over router + nodes
