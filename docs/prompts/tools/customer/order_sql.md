# Order SQL Prompt

Generate SQL for order queries.

## Location

`prompts/tools/customer/order_sql.prompt`

## Prompt Name

`tools_customer_order_sql`

## Purpose

Generate SELECT queries for customer order history.

## Input Variables

| Variable | Description |
|----------|-------------|
| `question` | User's order question |
| `customer_id` | Current customer ID |
| `schema` | Database schema |
| `db_type` | sqlite or postgresql |

## Output Format

```json
{
  "sql": "SELECT ...",
  "explanation": "Brief explanation"
}
```

## Key Rules

| Rule | Description |
|------|-------------|
| Customer filter | MUST include `customer_id = X` in WHERE |
| Privacy | Only show current customer's orders |
| SELECT only | No INSERT, UPDATE, DELETE |
| Include order_id | Always return order_id for cancel operations |
