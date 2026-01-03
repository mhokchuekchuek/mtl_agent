# TODO: Cancel Order Feature

## Issue
Customer chatbot สามารถสั่งซื้อ (place_order) ได้ แต่ไม่สามารถยกเลิก order ได้ ซึ่งไม่ make sense จาก UX perspective

## Current Behavior
- User ขอยกเลิก order → Chatbot บอกให้ติดต่อ customer service
- ไม่มี cancel_order tool

## Why Not Implemented Now
1. **Database schema ไม่รองรับ** - Orders table ไม่มี `status` column
   ```sql
   CREATE TABLE Orders (
     order_id INTEGER,
     order_date TIMESTAMP,
     customer_id INTEGER,
     total_amount INTEGER
   );
   ```
2. **Scope ใหญ่** - ต้องแก้หลายส่วน
3. **Time constraint** - อยู่นอก scope ของ evaluation improvement round

## Implementation Plan

### 1. Update Database Schema
```sql
ALTER TABLE Orders ADD COLUMN status TEXT DEFAULT 'completed';
-- Possible values: 'pending', 'completed', 'cancelled', 'refunded'
```

### 2. Create CancelOrderSQLTool
- File: `src/modules/tools/knowledge_retrieval/sql/customer/cancel_order.py`
- Validate order belongs to current customer
- Check if order is cancellable (e.g., status = 'pending', within 24 hours)
- Update status to 'cancelled'
- Restore product stock (UPDATE Products SET stock_quantity = stock_quantity + cancelled_qty)

### 3. Create Cancel Order Prompt
- File: `prompts/tools/customer/cancel_order_sql.prompt`

### 4. Update Product Agent Prompt
- Add cancel_order_sql to available tools
- Add workflow for cancellation requests

### 5. Add Test Cases
- Cancel own order (should succeed)
- Cancel other customer's order (should refuse)
- Cancel already shipped order (should refuse)
- Cancel order older than 24 hours (business rule)

## Priority
Medium - Nice to have for complete UX, but not critical for MVP
