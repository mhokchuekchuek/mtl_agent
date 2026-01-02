-- Migration: 002_fix_orders_primary_key
-- Date: 2026-01-02
-- Description: Fix Orders table to have proper PRIMARY KEY AUTOINCREMENT and clean NULL order_ids

-- Step 1: Delete orders with NULL order_id (these are test orders)
DELETE FROM Orders WHERE order_id IS NULL;

-- Step 2: Create new Orders table with proper schema
CREATE TABLE Orders_new (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TIMESTAMP,
    customer_id INTEGER,
    total_amount INTEGER,
    status TEXT DEFAULT 'completed'
);

-- Step 3: Copy existing data
INSERT INTO Orders_new (order_id, order_date, customer_id, total_amount, status)
SELECT order_id, order_date, customer_id, total_amount, status FROM Orders;

-- Step 4: Drop old table
DROP TABLE Orders;

-- Step 5: Rename new table
ALTER TABLE Orders_new RENAME TO Orders;

-- Step 6: Reset autoincrement to continue from max order_id
-- SQLite will automatically use MAX(order_id) + 1 for next insert
