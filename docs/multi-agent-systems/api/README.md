# API Overview

REST API layer for MTL Agent chatbots.

## Architecture

```
FastAPI App
    ├── /api/v1/chatbot/customer  → CustomerChatbotService
    └── /api/v1/chatbot/client    → ClientChatbotService
```

## Structure

| Path | Purpose |
|------|---------|
| `src/api/routes/chatbots/customer.py` | Customer chatbot endpoints |
| `src/api/routes/chatbots/client.py` | Client chatbot endpoints |
| `src/api/schemas/chatbots/customer.py` | Customer request/response models |
| `src/api/schemas/chatbots/client.py` | Client request/response models |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Router Organization | Separated by domain, uses versioning prefix `/api/v1/...` |
| Service Injection | Services initialize in `lifespan`, stored in `app.state` |
| Error Handling | Catch exceptions, return HTTP 500 with error message |

## Endpoints

| Endpoint | Description |
|----------|-------------|
| [POST /api/v1/chatbot/customer/chat](endpoints/customer-chat.md) | Customer chatbot |
| [POST /api/v1/chatbot/client/chat](endpoints/client-chat.md) | Client chatbot (internal BI) |
