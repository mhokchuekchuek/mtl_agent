# CustomerInsightAgent

ReAct agent for BI analytics and visualizations.

## Location
`src/modules/agents/client/insight.py`

## Purpose

Analyzes business data from SQLite ERP database and creates visualizations.

## Tools
- `SQLTool` with SQLiteClient - query ERP data
- `VisualizationTool` - create Plotly charts

## Database Tables (SQLite)
- Orders, OrderDetails
- Customers
- Products
- Inventory, Warehouses

## Usage

```python
from src.modules.agents.client.insight import CustomerInsightAgent

agent = CustomerInsightAgent(
    llm=chat_openai,
    prompt_manager=prompt_manager,
    tools=[sql_tool_sqlite, visualization_tool],
    prompt_name="client_chatbot_insight",
    max_iterations=5,
)

result = agent.execute({"translated_query": "Show sales by category"})
# result = {
#     "response": "Total sales by category...",
#     "chart_html": "<div>...</div>"
# }
```

## Output
- `response` - text analysis
- `chart_html` - Plotly HTML (optional)

## Config
`configs/agents/client_chatbot.yaml` → `agents.insight`
