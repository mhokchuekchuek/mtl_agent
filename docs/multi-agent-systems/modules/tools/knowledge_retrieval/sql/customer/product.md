# Customer Product SQL Tool

Product and inventory queries for customers.

## Location

`src/modules/tools/knowledge_retrieval/sql/customer/product.py`

## Class: CustomerProductSQLTool

Inherits from `SQLTool`.

### Purpose

Query product information - details, prices, stock levels, and inventory. Restricted to product-related tables only.

### Configuration

| Property | Value |
|----------|-------|
| Tables | Products, Inventory (restricted) |
| Write | No (read-only) |
| Filter | `allowed_tables` validation |
| Prompt | `tools_customer_product_sql` |

### Input Schema

| Field | Type | Description |
|-------|------|-------------|
| `question` | str | Question about products or inventory |

### Code Flow

```mermaid
flowchart TD
    A[1. Get Prompt from Langfuse] --> B[2. Compile prompt with filtered schema + question]
    B --> C[3. LLM generates SQL]
    C --> D[4. Validate SQL is safe]
    D --> E[5. Validate only allowed tables accessed]
    E --> F[6. Execute SQL on database]
    F --> G[7. Return product results]
```

### Security

- **Schema filtering**: Only Products and Inventory tables shown to LLM
- **Table validation**: Rejects queries accessing Orders, Customers, etc.

### Usage

```python
from src.modules.tools.knowledge_retrieval.sql.customer.product import CustomerProductSQLTool

tool = CustomerProductSQLTool(
    sql_client=sql_client,
    llm_client=llm_client,
    prompt_manager=prompt_manager,
    allowed_tables=["Products", "Inventory", "Warehouses"],
)

# Example queries
tool._run("Show me all laptops under $1000")
tool._run("Is the iPhone 15 in stock?")
```

### Example Questions

- "Show me all laptops under $1000"
- "Is the iPhone 15 in stock?"
- "What colors are available for product X?"
- "Which products are on sale?"
