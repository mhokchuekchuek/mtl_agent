# Cancel Order SQL Prompt

Generate SQL statements for cancelling customer orders.

## Location

`prompts/tools/customer/cancel_order_sql.prompt`

## Prompt Name

`tools_customer_cancel_order_sql`

## Purpose

Generate SQL statements to:
1. Verify order ownership
2. Check order status
3. Get order details for inventory restoration
4. Update status to cancelled
5. Restore inventory quantities

## Input Variables

| Variable | Description |
|----------|-------------|
| `order_id` | Order ID to cancel |
| `customer_id` | Customer requesting cancellation |
| `schema` | Database schema |
| `db_type` | sqlite or postgresql |

## Output Format

```json
{
  "check_order": "SELECT ... WHERE order_id = X AND customer_id = Y",
  "check_status": "SELECT status FROM Orders WHERE ...",
  "get_order_details": "SELECT product_id, quantity, color FROM OrderDetails WHERE ...",
  "update_status": "UPDATE Orders SET status = 'cancelled' WHERE ...",
  "restore_inventory": "UPDATE Inventory SET quantity = quantity + ..."
}
```

## Flow

```mermaid
flowchart TD
    A[1. check_order] --> B{Belongs to customer?}
    B -->|No| ERR1[Return error]
    B -->|Yes| C[2. check_status]
    C --> D{Already cancelled?}
    D -->|Yes| ERR2[Return error]
    D -->|No| E[3. get_order_details]
    E --> F[4. update_status]
    F --> G[5. restore_inventory]
    G --> OK[Cancellation complete]
```

## Key Rules

| Rule | Description |
|------|-------------|
| Security | MUST verify customer_id ownership |
| Color matching | Restore to same color inventory row |
| SUM quantity | Handle multiple OrderDetails rows |
| NULL handling | Handle NULL color values |
