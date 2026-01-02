-- Migration: 001_add_order_status
-- Date: 2025-12-31
-- Description: Add status column to Orders table for cancel order feature

-- Add status column with default 'completed' for existing orders
ALTER TABLE Orders ADD COLUMN status TEXT DEFAULT 'completed';

-- Possible status values:
-- 'pending'   - Order placed, awaiting processing
-- 'completed' - Order processed/shipped
-- 'cancelled' - Order cancelled by customer
-- 'refunded'  - Order refunded

-- Note: All existing orders will have status = 'completed'
