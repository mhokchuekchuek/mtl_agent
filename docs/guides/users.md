# **👤 Users Guide**

Guide for end users and business users who want to use the chatbot.


---


## **📋 Parameters**

These parameters are used by both UI and API:

| Parameter | Purpose |
|-----------|---------|
| `thread_id` | Conversation ID for multi-turn chat |
| `user_id` | Customer ID (1-100) for order operations |

> 💡 **Tip:** Use the same `thread_id` for follow-up questions to maintain context.


---


## **🤖 Chatbots**

| Chatbot | Purpose | Port |
|---------|---------|------|
| Customer Chatbot | Product search, orders, support | 8501 |
| Client Chatbot | BI analytics, reports, visualizations | 8502 |


---


## **👤 Customer Chatbot**

**Features**: Product search, stock/price check, place/cancel orders, view orders

**Example Queries**:
- "Do you have gaming products?"
- "I want to order 2 Gaming Chairs"
- "Cancel my order #123"

**Screenshots**: [Customer App](../multi-agent-systems/ui/customer_app.md#screenshots)

**API**: [Customer Chat API](../multi-agent-systems/api/customer_chat.md)


---


## **💼 Client Chatbot**

**Features**: Sales analytics, revenue reports, visualizations, chat history lookup

**Example Queries**:
- "Show me this month's sales"
- "Revenue by category as a chart"
- "What did customer 123 ask yesterday?"

**Screenshots**: [Client App](../multi-agent-systems/ui/client_app.md#screenshots)

**API**: [Client Chat API](../multi-agent-systems/api/client_chat.md)


---


## **🔗 API Usage**


### 📤 **Request**

```bash
curl -X POST http://localhost:8000/api/v1/chatbot/{customer|client}/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "thread_id": "session-123", "user_id": "15"}'
```
