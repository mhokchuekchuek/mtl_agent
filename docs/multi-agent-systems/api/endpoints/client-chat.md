# POST /api/v1/chatbot/client/chat

Chat with client chatbot for internal BI (chat history lookup, insights).

## Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | User message (Thai or English) |
| thread_id | string | Yes | Conversation thread ID |
| user_id | string | No | User identifier |

## Response

| Field | Type | Description |
|-------|------|-------------|
| response | string | Chatbot response |
| thread_id | string | Conversation thread ID |
| intent | string | Detected intent (`chat_history` or `insight`) |
| chart_html | string | Plotly chart HTML (if visualization created) |

## Example

```bash
curl -X POST http://localhost:8000/api/v1/chatbot/client/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "แสดงยอดขายรายเดือน", "thread_id": "test-456"}'
```

## Errors

| Status | Description |
|--------|-------------|
| 500 | Internal server error |
