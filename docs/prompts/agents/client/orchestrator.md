# Orchestrator Prompt

Route client queries to appropriate agents.

## Location

`prompts/agents/client/orchestrator.prompt`

## Prompt Name

`client_chatbot_orchestrator`

## Purpose

Classify user intent to route to either `chat_history` or `insight` agent.

## Input Variables

| Variable | Description |
|----------|-------------|
| `current_datetime` | Current date/time |
| `timezone` | Current timezone |

## Output

Single word: `chat_history` or `insight`

## Categories

```mermaid
flowchart TD
    Q[User Query] --> C{Classify Intent}
    C -->|Conversation logs| CH[chat_history]
    C -->|Business data| IN[insight]
    
    CH --> EX1["Find conversations with customer 12345"]
    CH --> EX2["What did the customer ask yesterday?"]
    
    IN --> EX3["Show customer details for John"]
    IN --> EX4["What are top selling products?"]
    IN --> EX5["Create chart of monthly revenue"]
```

| Category | When to Use | Examples |
|----------|-------------|----------|
| `chat_history` | Search conversation logs | "Find conversations with customer ID 12345" |
| `insight` | Query business data, analytics, reports | "Show sales by region", "Customer profile" |

## Key Rules

- Queries about customer **profiles, orders, business data** → `insight`
- Queries about **chat conversation history** → `chat_history`
