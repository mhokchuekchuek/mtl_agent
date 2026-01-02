# OrchestratorAgent

Router agent that classifies user intent for client chatbot.

## Location
`src/modules/agents/client/orchestrator.py`

## Purpose

Decides whether user query should go to:
- `CustomerChatHistoryAgent` - for chat history lookup
- `CustomerInsightAgent` - for BI analytics

## Intents

### `chat_history`
- Looking up customer conversations
- Searching chat history by customer ID, name, date

### `insight`
- Analyzing business data
- Creating reports/visualizations
- Querying sales, orders, inventory

## Usage

```python
from src.modules.agents.client.orchestrator import OrchestratorAgent, Intent

agent = OrchestratorAgent(
    llm=chat_openai,
    prompt_manager=prompt_manager,
    prompt_name="client_chatbot_orchestrator",
)

result = agent.execute({"translated_query": "Show me sales this month"})
# result = {"intent": Intent.INSIGHT}
```

## Config
`configs/agents/client_chatbot.yaml` → `agents.orchestrator`
