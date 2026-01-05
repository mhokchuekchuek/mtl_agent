# **💬 Chat History SQL Prompt**

Generate SQL for querying chat conversation history.


---


## **📍 Location**

[`prompts/tools/client/chat_history_sql.prompt`](../../../../prompts/tools/client/chat_history_sql.prompt)


---


## **🏷️ Prompt Name**

`client_chatbot_chat_history_sql`


---


## **💡 Purpose**

Generate SQL queries to search and analyze customer chat conversations stored in PostgreSQL.


---


## **📥 Input Variables**

| Variable | Description |
|----------|-------------|
| `question` | User's query about chat history |
| `schema` | Database schema definition |


---


## **📤 Output Format**

JSON object with SQL and explanation:

```json
{
  "sql": "SELECT ...",
  "explanation": "Brief explanation"
}
```


---


## **🗄️ Store Table Schema**

| Column | Type | Description |
|--------|------|-------------|
| `key` | text | Unique conversation/message ID |
| `value` | JSONB | Message content (query, response, thread_id, timestamp) |
| `prefix` | text | Namespace: `users.{customer_id}.conversations` |
| `created_at` | timestamp | Creation time |
| `updated_at` | timestamp | Last update time |


---


## **🔧 JSONB Operators**

| Operator | Usage | Example |
|----------|-------|---------|
| `->>` | Extract text | `value->>'query'` |
| `ILIKE` | Case-insensitive search | `value->>'query' ILIKE '%%keyword%%'` |


---


## **📋 Query Patterns**

| Goal | Pattern |
|------|---------|
| All customers | `prefix LIKE 'users.%%.conversations'` |
| Specific customer | `prefix = 'users.{id}.conversations'` |
| Search content | `value->>'query' ILIKE '%%term%%'` |


---


## **📝 Rules**

1. READ-ONLY: Only SELECT queries allowed
2. Use `%%` (double percent) for LIKE patterns (driver escaping)
3. Use JSONB operators for value field access
4. Use `created_at` for time-based queries
