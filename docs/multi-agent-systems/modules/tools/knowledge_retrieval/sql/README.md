# SQL Tools

Natural language to SQL query tools for the multi-agent system.

## Overview

SQL tools generate and execute SQL queries from natural language questions. They use LLM to convert questions to SQL, validate for security, and execute against the database.

## Architecture

```
src/modules/tools/knowledge_retrieval/sql/
├── base/                    # Base SQL tool class
│   ├── main.py             # SQLTool base class
│   └── validator.py        # SQL security validator
├── client/                  # Client chatbot tools
│   ├── analytics.py        # BI analytics (all tables, read-only)
│   └── chat_history.py     # Chat history queries (PostgreSQL)
└── customer/                # Customer chatbot tools
    ├── product.py          # Product queries (restricted tables)
    ├── order.py            # Order history (customer_id filtered)
    ├── place_order.py      # Place orders (write enabled)
    └── cancel_order.py     # Cancel orders (write enabled)
```

## Tool Hierarchy

| Tool | Inherits | Tables | Write | Filter |
|------|----------|--------|-------|--------|
| SQLTool (base) | BaseTool | All | Configurable | None |
| ClientAnalyticsSQLTool | SQLTool | All | No | None |
| ClientChatHistorySQLTool | SQLTool | store | No | None |
| CustomerProductSQLTool | SQLTool | Products, Inventory | No | allowed_tables |
| CustomerOrderSQLTool | SQLTool | Orders, OrderDetails | No | customer_id |
| PlaceOrderSQLTool | SQLTool | Orders, OrderDetails, Inventory | Yes | customer_id |
| CancelOrderSQLTool | SQLTool | Orders | Yes | customer_id |

## Security

All tools use `SQLValidator` which:
- **Always blocks**: DDL (DROP, ALTER, CREATE), permissions (GRANT, REVOKE), execution (EXEC)
- **Blocks when read-only**: DML (INSERT, UPDATE, DELETE)
- **Blocks patterns**: Multiple statements (`;`), comments (`--`, `/*`)

Customer tools add additional restrictions:
- **Table filtering**: Only allowed tables visible in schema
- **Customer isolation**: Queries must include customer_id filter

## Documentation

---

### base

| File | Description |
|------|-------------|
| [main.md](base/main.md) | SQLTool base class |
| [validator.md](base/validator.md) | SQL security validator |

### client

| File | Description |
|------|-------------|
| [analytics.md](client/analytics.md) | BI analytics tool (all tables, read-only) |
| [chat_history.md](client/chat_history.md) | Chat history queries |

### customer

| File | Description |
|------|-------------|
| [product.md](customer/product.md) | Product queries (restricted tables) |
| [order.md](customer/order.md) | Order history (customer_id filtered) |
| [place_order.md](customer/place_order.md) | Place orders (write enabled) |
| [cancel_order.md](customer/cancel_order.md) | Cancel orders (write enabled) |
