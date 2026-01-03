# Dependencies

Dependency injection wiring layer.

## Location

`src/dependencies/`

## Overview

Dependencies layer creates and wires all components together. Each file provides a `build_*_service()` function that returns a ready-to-use service.

```mermaid
flowchart TD
    subgraph Dependencies
        D[build_chatbot_service]
    end
    
    subgraph Creates
        C[Clients]
        R[Repositories]
        T[Tools]
        A[Agents]
        W[Workflow]
        S[Service]
    end
    
    D --> C
    D --> R
    D --> T
    D --> A
    D --> W
    D --> S
```

## Available Dependencies

| File | Function | Documentation |
|------|----------|---------------|
| client_chatbot.py | `build_client_chatbot_service()` | [client_chatbot.md](client_chatbot.md) |
| customer_chatbot.py | `build_chatbot_service()` | [customer_chatbot.md](customer_chatbot.md) |

## Config Loading

Dependencies read from `configs/agents/`:

| Config File | Documentation |
|-------------|---------------|
| shared.yaml | [configs/shared.md](../configs/shared.md) |
| client_chatbot.yaml | [configs/client_chatbot.md](../configs/client_chatbot.md) |
| customer_chatbot.yaml | [configs/customer_chatbot.md](../configs/customer_chatbot.md) |

## References

- [Usecases](../usecases/README.md) - Business logic layer
- [Repositories](../repositories/README.md) - Data access layer
