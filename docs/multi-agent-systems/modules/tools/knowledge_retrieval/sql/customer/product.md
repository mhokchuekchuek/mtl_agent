# Customer Product SQL Tool

Product and inventory queries for customers.

## Location

`src/modules/tools/knowledge_retrieval/sql/customer/product.py`

## Prompt

[tools_customer_product_sql](../../../../../prompts/tools/customer/product_sql.md)

## Overview

Query product information - details, prices, stock levels. **Read-only** tool restricted to product-related tables.

## Input

| Field | Type | Description |
|-------|------|-------------|
| `question` | str | Question about products or inventory |

## Flow Diagram

```mermaid
flowchart TD
    START[Customer asks about products] --> PROMPT[1. Load prompt from Langfuse]
    
    PROMPT --> SCHEMA[2. Get schema for allowed tables only]
    SCHEMA --> |Products, Inventory| COMPILE[3. Compile prompt]
    
    COMPILE --> LLM[4. LLM generates SQL]
    LLM --> VALIDATE[5. Validate SQL]
    
    VALIDATE --> CHECK_TABLES{Tables allowed?}
    CHECK_TABLES --> |No| REJECT[Reject: Forbidden table access]
    
    CHECK_TABLES --> |Yes| CHECK_SAFE{SQL is safe?}
    CHECK_SAFE --> |No| REJECT2[Reject: Security violation]
    
    CHECK_SAFE --> |Yes| EXECUTE[6. Execute SQL]
    EXECUTE --> |Query| PROD_TBL[(Products)]
    EXECUTE --> |Query| INV_TBL[(Inventory)]
    
    PROD_TBL --> RESULTS[7. Return results]
    INV_TBL --> RESULTS
```

## Database Access

### Allowed Tables (Read-Only)

| Table | Columns | Description |
|-------|---------|-------------|
| Products | product_id, product_name, category, price, description | Product catalog |
| Inventory | product_id, quantity, color, warehouse_id | Stock levels |

### Forbidden Tables

| Table | Reason |
|-------|--------|
| Customers | Privacy - customer data |
| Orders | Privacy - other customers' orders |
| OrderDetails | Privacy - order details |

### Security Validation

```mermaid
flowchart LR
    SQL[Generated SQL] --> V1{Contains forbidden table?}
    V1 --> |Yes| FAIL[Reject]
    V1 --> |No| V2{Has dangerous keywords?}
    V2 --> |Yes| FAIL
    V2 --> |No| PASS[Execute]
```

Blocked patterns:
- `DROP`, `DELETE`, `UPDATE`, `INSERT` (write operations)
- Access to Customers, Orders, OrderDetails tables

## Example

### Input
```
Customer: Is the Gaming Chair in stock?
```

### Generated SQL
```sql
SELECT p.product_name, i.quantity, i.color
FROM Products p
JOIN Inventory i ON p.product_id = i.product_id
WHERE p.product_name LIKE '%Gaming Chair%'
```

### Database Query

| Table | Operation | Purpose |
|-------|-----------|---------|
| Products | SELECT | Get product name, price |
| Inventory | SELECT | Get stock quantity by color |

### Response
```python
{
    "sql": "SELECT p.product_name, i.quantity, i.color FROM Products p JOIN Inventory i ON p.product_id = i.product_id WHERE p.product_name LIKE '%Gaming Chair%'",
    "results": [
        {"product_name": "Gaming Chair", "quantity": 24, "color": "Gold"}
    ]
}
```

**Database Changes**: None (read-only)

## Example Questions

| Question | Tables Accessed |
|----------|-----------------|
| "Show me all laptops under $1000" | Products |
| "Is the iPhone 15 in stock?" | Products, Inventory |
| "What colors are available for Gaming Chair?" | Products, Inventory |
| "How many products do you have?" | Products |

## Error Cases

| Error | Cause | Response |
|-------|-------|----------|
| Forbidden table access | Query tries to access Orders/Customers | Reject with error message |
| SQL security violation | Contains DROP/DELETE/UPDATE | Reject with error message |

## References

- [CustomerProductSQLTool](../../../../../../src/modules/tools/knowledge_retrieval/sql/customer/product.py)
