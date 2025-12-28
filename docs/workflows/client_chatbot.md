# ClientChatbotWorkflow

Internal BI chatbot workflow for business users (Thai + English).

## Location
`src/modules/workflows/client_chatbot/main.py`

## Architecture

```
User Query → TranslationAgent → Orchestrator (Router)
                                      ↓
                         ┌────────────┴────────────┐
                         ↓                         ↓
            CustomerChatHistoryAgent      CustomerInsightAgent
                   (ReAct)                     (ReAct)
                      ↓                           ↓
                  SQLTool                     SQLTool
                (PostgreSQL)                 (SQLite)
                                                  ↓
                                          VisualizationTool
                                      ↓
                              TranslationAgent (output)
```

## Use Cases

### 1. Lookup Customer Chat
Query: "ดูประวัติแชทของลูกค้า ID 123"
- Routes to `CustomerChatHistoryAgent`
- Queries PostgreSQL `store` table

### 2. Customer Insight (BI)
Query: "ยอดขายเดือนนี้แยกตาม category"
- Routes to `CustomerInsightAgent`
- Queries SQLite ERP data
- Creates Plotly visualization

## State
`ClientChatbotState` includes:
- `query`, `translated_query`, `user_language`
- `intent` (chat_history | insight)
- `response`, `chart_html`, `error`

## Files
- State: `src/modules/workflows/client_chatbot/state.py`
- Workflow: `src/modules/workflows/client_chatbot/main.py`
- Repository: `src/repositories/chatbots/client/main.py`
- Dependencies: `src/dependencies/client_chatbot.py`
- Config: `configs/agents/client_chatbot.yaml`
- Prompts: `prompts/client_chatbot/`
