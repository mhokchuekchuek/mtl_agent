# **💬 Chat History Agent Prompt**

System prompt for the customer chat history lookup agent.


---


## **🏷️ Langfuse Name**

`client_chatbot_chat_history`


---


## **📍 Location**

[`prompts/agents/client/chat_history.prompt`](../../../prompts/agents/client/chat_history.prompt)


---


## **🔗 Used By**

- [CustomerChatHistoryAgent](../../../multi-agent-systems/modules/agents/client/chat_history.md)


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
1. Understand user's chat history search criteria
2. Query PostgreSQL store table with JSONB operations
3. Parse and format conversation results
4. Present findings chronologically


---


## **📝 Key Instructions**

- **Database**: PostgreSQL with JSONB `store` table
- **JSONB Access**: Use `->` and `->>` operators
- **Search**: Use `LIKE` on `value::text` for keyword search
- **Output**: Format conversations chronologically
