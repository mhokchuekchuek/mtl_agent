# Evaluation Loop - Round 2

## วิธี Loop ผ่าน Evaluation Results

### Step 1: ดู Summary
```bash
cat results/client/summary.csv
```

### Step 2: อ่าน Failed Test Details
```bash
cat results/client/<use_case>/<turn_type>/<test_id>/results.yaml
cat results/client/<use_case>/<turn_type>/<test_id>/detail.yaml
```

### Step 3: Lookup Real DB (ถ้าสงสัย)

**SQLite (ERP Database):**
```bash
sqlite3 data/erp_database.db "SELECT * FROM Customers LIMIT 5"
sqlite3 data/erp_database.db ".schema Customers"
sqlite3 data/erp_database.db ".tables"
```

**PostgreSQL (Chat History):**
```bash
psql -h localhost -U postgres -d langgraph -c "SELECT * FROM store LIMIT 5"
psql -h localhost -U postgres -d langgraph -c "\d store"
```

### Step 4: วิเคราะห์สาเหตุ

| สาเหตุ | ตัวอย่าง |
|--------|----------|
| **Code** | Tool ทำงานผิด, logic error |
| **Prompt** | Agent เรียก tool ผิด, generate SQL ผิด |
| **Dataset** | Test case / expected ผิด |
| **Judge** | Judge ให้คะแนนผิด |

### Step 5: Update Status Table

---

## Client Chatbot - Failed Tests

### Analytics

| Test Case | Score | Part | Status | How to Solve |
|-----------|-------|------|--------|--------------|
| `monthly_revenue` | 0.65 | | | |
| `top_customers` | 0.0 | | | |
| `total_revenue_this_month` | 0.24 | | | |
| `customer_analysis` | 0.51 | | | |

### Visualizations

| Test Case | Score | Part | Status | How to Solve |
|-----------|-------|------|--------|--------------|
| `line_chart_monthly_revenue` | 0.0 | | | |
| `chart_then_modify` | 0.0 | | | |

### Customer Insights

| Test Case | Score | Part | Status | How to Solve |
|-----------|-------|------|--------|--------------|
| `specific_customer_info` | 0.0 | | | |
| `specific_customer_orders` | 0.0 | | | |
| `specific_product_info` | 0.0 | | | |
| `category_drill_down` | 0.5 | | | |

### Chat History

| Test Case | Score | Part | Status | How to Solve |
|-----------|-------|------|--------|--------------|
| `search_topic_in_chats` | 0.65 | | | |

---

## Summary

| Category | Passed | Failed | Total |
|----------|--------|--------|-------|
| Analytics | 3 | 4 | 7 |
| Visualizations | 4 | 2 | 6 |
| Customer Insights | 2 | 4 | 6 |
| Chat History | 2 | 1 | 3 |
| Negative | 6 | 0 | 6 |
| **Total** | **17** | **11** | **28** |
