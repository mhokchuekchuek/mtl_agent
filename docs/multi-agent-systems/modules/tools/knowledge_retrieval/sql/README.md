# **🔷 SQL Tools**

Natural language to SQL query tools for the multi-agent system.


---


## **📋 Overview**

SQL tools generate and execute SQL queries from natural language questions. They use LLM to convert questions to SQL, validate for security, and execute against the database.


---


## **🏗️ Architecture**

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


---


## **📊 Tool Hierarchy**

| Tool | Inherits | Tables | Write | Filter |
|------|----------|--------|-------|--------|
| SQLTool (base) | BaseTool | All | Configurable | None |
| ClientAnalyticsSQLTool | SQLTool | All | No | None |
| ClientChatHistorySQLTool | SQLTool | store | No | None |
| CustomerProductSQLTool | SQLTool | Products, Inventory | No | allowed_tables |
| CustomerOrderSQLTool | SQLTool | Orders, OrderDetails | No | customer_id |
| PlaceOrderSQLTool | SQLTool | Orders, OrderDetails, Inventory | Yes | customer_id |
| CancelOrderSQLTool | SQLTool | Orders | Yes | customer_id |


---


## **🔒 Security**

> 🚨 **Warning:** All tools use `SQLValidator` for security.

All tools use `SQLValidator` which:
- **Always blocks**: DDL (DROP, ALTER, CREATE), permissions (GRANT, REVOKE), execution (EXEC)
- **Blocks when read-only**: DML (INSERT, UPDATE, DELETE)
- **Blocks patterns**: Multiple statements (`;`), comments (`--`, `/*`)

Customer tools add additional restrictions:
- **Table filtering**: Only allowed tables visible in schema
- **Customer isolation**: Queries must include customer_id filter


---


## **📖 Documentation**


### 🎯 **base**

| | |
|:---:|:---:|
| [🎯 **Main**](base/main.md)<br/>SQLTool base class | [🔒 **Validator**](base/validator.md)<br/>SQL security validator |


### 💼 **client**

| | |
|:---:|:---:|
| [📊 **Analytics**](client/analytics.md)<br/>BI analytics tool (all tables, read-only) | [💬 **Chat History**](client/chat_history.md)<br/>Chat history queries |


### 👤 **customer**

| | | |
|:---:|:---:|:---:|
| [🛍️ **Product**](customer/product.md)<br/>Product queries (restricted tables) | [📦 **Order**](customer/order.md)<br/>Order history (customer_id filtered) | [🛒 **Place Order**](customer/place_order.md)<br/>Place orders (write enabled) |
| [❌ **Cancel Order**](customer/cancel_order.md)<br/>Cancel orders (write enabled) | | |
