# **📊 Insight Agent Prompt**

System prompt for the customer insight and BI analytics agent.


---


## **🏷️ Langfuse Name**

`client_chatbot_insight`


---


## **📍 Location**

[`prompts/agents/client/insight.prompt`](../../../../prompts/agents/client/insight.prompt)


---


## **🔗 Used By**

- [CustomerInsightAgent](../../../multi-agent-systems/modules/agents/client/insight.md)


---


## **🤖 Model**

`gpt-4o-mini`


---


## **📥 Variables**

| Variable | Type | Description |
|----------|------|-------------|
| `current_datetime` | string | Current date/time for context |
| `timezone` | string | Timezone for date interpretation |


---


## **💡 Purpose**

Guide the agent to:
1. Understand user's analytical questions
2. Query SQLite ERP database for business data
3. Analyze results and identify insights
4. Create visualizations when appropriate


---


## **📝 Key Instructions**

- **Database**: SQLite with ERP tables (Orders, Customers, Products, etc.)
- **Read-Only**: Only SELECT statements allowed
- **Visualization**: Always use `create_visualization` tool, never generate chart code
- **Context**: Remember previous queries for follow-up questions


---


## **🗄️ Schema**

Available tables:
- Orders, OrderDetails
- Customers, Products
- Inventory, Warehouses
