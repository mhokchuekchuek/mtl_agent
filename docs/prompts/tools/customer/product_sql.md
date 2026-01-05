# **🛍️ Product SQL Prompt**

Generate SQL for product queries.


---


## **📍 Location**

[`prompts/tools/customer/product_sql.prompt`](../../../../prompts/tools/customer/product_sql.prompt)


---


## **🏷️ Prompt Name**

`customer_chatbot_product_sql`


---


## **💡 Purpose**

Generate SELECT queries for product information (prices, stock, categories).


---


## **📥 Input Variables**

| Variable | Description |
|----------|-------------|
| `question` | User's product question |
| `schema` | Database schema |
| `db_type` | sqlite or postgresql |


---


## **📤 Output Format**

```json
{
  "sql": "SELECT ...",
  "explanation": "Brief explanation"
}
```


---


## **✅ Allowed Tables**

- Products
- Inventory
- Warehouses


---


## **🚫 Forbidden Tables**

- Customers
- Orders
- OrderDetails


---


## **📝 Key Rules**

| Rule | Description |
|------|-------------|
| Stock queries | Use `SUM(quantity)` for total stock |
| Category search | Use `LIKE '%category%'` for flexible matching |
| SELECT only | No INSERT, UPDATE, DELETE |
| Schema columns | Use ONLY columns in schema |
