# POST /api/v1/chatbot/customer/chat

Chat with customer chatbot for product inquiries.

## Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | User message |
| thread_id | string | Yes | Conversation thread ID |
| user_id | string | No | User identifier |

## Response

| Field | Type | Description |
|-------|------|-------------|
| response | string | Chatbot response |
| thread_id | string | Conversation thread ID |

## Example

```bash
curl -X POST http://localhost:8000/api/v1/chatbot/customer/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "สินค้าประกันชีวิตมีอะไรบ้าง", "thread_id": "test-123"}'
```

## Errors

| Status | Description |
|--------|-------------|
| 500 | Internal server error |
