# Customer Order SQL Tool

Order history queries for customers.

## Location

`src/modules/tools/knowledge_retrieval/sql/customer/order.py`

## Prompt

[tools_customer_order_sql](../../../../../prompts/tools/customer/order_sql.md)

## Overview

Query customer's own order history - order status, purchase history. **Read-only** tool that automatically filters by customer_id.

## Input

| Field | Type | Description |
|-------|------|-------------|
| `question` | str | Question about your orders |

## Flow Diagram

```mermaid
flowchart TD
    START[Customer asks about orders] --> CHECK_ID{customer_id set?}
    CHECK_ID --> |No| ERROR[Error: Customer ID not set]
    
    CHECK_ID --> |Yes| PROMPT[1. Load prompt from Langfuse]
    PROMPT --> SCHEMA[2. Get schema for allowed tables]
    SCHEMA --> |Orders, OrderDetails, Products| COMPILE[3. Compile prompt with customer_id]
    
    COMPILE --> LLM[4. LLM generates SQL with customer_id filter]
    LLM --> VALIDATE[5. Validate SQL]
    
    VALIDATE --> CHECK_TABLES{Tables allowed?}
    CHECK_TABLES --> |No| REJECT[Reject: Forbidden table]
    
    CHECK_TABLES --> |Yes| CHECK_FILTER{Has customer_id filter?}
    CHECK_FILTER --> |No| REJECT2[Reject: Missing customer filter]
    
    CHECK_FILTER --> |Yes| CHECK_SAFE{SQL is safe?}
    CHECK_SAFE --> |No| REJECT3[Reject: Security violation]
    
    CHECK_SAFE --> |Yes| EXECUTE[6. Execute SQL]
    EXECUTE --> |Query| ORDERS_TBL[(Orders)]
    EXECUTE --> |Query| DETAILS_TBL[(OrderDetails)]
    
    ORDERS_TBL --> RESULTS[7. Return results]
    DETAILS_TBL --> RESULTS
```

## Database Access

### Allowed Tables (Read-Only)

| Table | Columns | Description |
|-------|---------|-------------|
| Orders | order_id, customer_id, order_date, status, total_amount | Order headers |
| OrderDetails | order_detail_id, order_id, product_id, quantity, unit_price | Order line items |
| Products | product_id, product_name, price | Product names for display |

### Automatic Filtering

All queries are automatically filtered by `customer_id`:

```sql
-- LLM always includes this filter
WHERE customer_id = {customer_id}
```

This prevents customers from seeing other customers' orders.

### Security Validation

```mermaid
flowchart LR
    SQL[Generated SQL] --> V1{Has customer_id filter?}
    V1 --> |No| FAIL[Reject: Missing filter]
    V1 --> |Yes| V2{Allowed tables only?}
    V2 --> |No| FAIL
    V2 --> |Yes| V3{Read-only?}
    V3 --> |No| FAIL
    V3 --> |Yes| PASS[Execute]
```

## Example

### Input
```
Customer: Show me my recent orders
```

### Generated SQL
```sql
SELECT o.order_id, o.order_date, o.status, o.total_amount
FROM Orders o
WHERE o.customer_id = '1'
ORDER BY o.order_date DESC
LIMIT 10
```

### Database Query

| Table | Operation | Purpose |
|-------|-----------|---------|
| Orders | SELECT | Get order list for this customer only |

### Response
```python
{
    "sql": "SELECT ... WHERE customer_id = '1' ...",
    "results": [
        {"order_id": 1001, "order_date": "2025-01-03", "status": "pending", "total_amount": 558},
        {"order_id": 998, "order_date": "2025-01-01", "status": "delivered", "total_amount": 1299}
    ]
}
```

**Database Changes**: None (read-only)

## Example Questions

| Question | Tables Accessed |
|----------|-----------------|
| "Show me my orders" | Orders |
| "What's the status of order #1001?" | Orders |
| "Show me what I ordered last month" | Orders, OrderDetails, Products |
| "How much did I spend this year?" | Orders |

## Privacy Protection

| Protection | How |
|------------|-----|
| Only own orders | SQL must contain `customer_id = {current_customer}` |
| No other customers | Cannot query without customer_id filter |
| Read-only | Cannot modify orders (use cancel_order tool instead) |

## Error Cases

| Error | Cause | Response |
|-------|-------|----------|
| Customer ID not set | Tool called without customer context | Error message |
| Missing customer filter | SQL doesn't filter by customer_id | Reject query |
| Forbidden table access | Query tries to access Customers table | Reject query |

## References

- [CustomerOrderSQLTool](../../../../../../src/modules/tools/knowledge_retrieval/sql/customer/order.py)
