# CustomerChatHistoryAgent

ReAct agent for looking up customer chat history from PostgreSQL.

## Location
`src/modules/agents/client/chat_history.py`

## Purpose

Queries LangGraph's `store` table to find customer conversations.

## Tools
- `SQLTool` with PostgreSQLClient

## Database
Queries `store` table (created by LangGraph PostgresStore):
- `namespace` - array of namespace components
- `key` - unique record key
- `value` - JSONB conversation data
- `created_at`, `updated_at` - timestamps

## Usage

```python
from src.modules.agents.client.chat_history import CustomerChatHistoryAgent

agent = CustomerChatHistoryAgent(
    llm=chat_openai,
    prompt_manager=prompt_manager,
    tools=[sql_tool_postgres],
    prompt_name="client_chatbot_chat_history",
    max_iterations=5,
)

result = agent.execute({"translated_query": "Find chat with customer 123"})
# result = {"response": "Found 3 conversations..."}
```

## Config
`configs/agents/client_chatbot.yaml` → `agents.chat_history`
