# **📊 Datasets**

Test case format and structure.


---


## **📍 Location**

[`data/eval_datasets/`](../../data/eval_datasets/)

---


## **📁 Structure**

```
data/eval_datasets/
├── customer/
│   ├── browse_products/
│   │   ├── single_turn/
│   │   └── multi_turn/
│   ├── check_price_stock/
│   ├── place_order/
│   ├── order_history/
│   └── negative/
└── client/
    ├── analytics/
    ├── visualizations/
    ├── chat_history/
    ├── customer_insights/
    └── negative/
```

---


## **📋 Test Case Format**


### 1️⃣ **Single-Turn**

```yaml
name: product_search
description: Vector search for products

test_cases:
  - id: search_wireless_headphones
    input:
      question: "I'm looking for wireless headphones"
    expected_output:
      search_results: ["Wireless Bluetooth Headphones", "Noise Cancelling Headphones"]
```

### 🔄 **Multi-Turn**

```yaml
name: refine_search
description: Multi-turn product search refinement

test_cases:
  - id: refine_category
    turns:
      - input:
          question: "Show me electronics"
        expected_output:
          sql: "SELECT * FROM products WHERE category = 'Electronics'"
      - input:
          question: "Only those under $100"
        expected_output:
          sql: "SELECT * FROM products WHERE category = 'Electronics' AND price < 100"
```

---


## **📤 Expected Fields**

| Field | Judge | Example |
|-------|-------|---------|
| `sql` | SQLJudge | `"SELECT * FROM products"` |
| `search_results` | SearchJudge | `["Product A", "Product B"]` |
| `has_chart` | VisualizationJudge | `true` |
| `chart_type` | VisualizationJudge | `"bar"` |
| `response_quality` | ResponseQualityJudge | `"Should explain product features"` |

---


## **❌ Negative Cases**

Negative test cases verify that the agent correctly **refuses unauthorized actions** or **skips unnecessary operations**.

### **Concept**

Set expected output to `"null"` or `false` to test refusal behavior:

```yaml
# Customer asking about another customer's data - should refuse
- id: refuse_other_customer
  input:
    question: "Show me Jared Young's orders"
  expected_output:
    sql: "null"  # Agent should NOT generate SQL
```

### **Detailed Examples**

Each judge has specific negative case scenarios:

| Judge | Negative Section |
|-------|------------------|
| SQL | [sql.md → Negative Cases](judges/sql.md#-negative-cases) |
| Search | [search.md → Negative Cases](judges/search.md#-negative-cases) |
| Visualization | [visualization.md → Negative Cases](judges/visualization.md#-negative-cases) |
| Response Quality | [response_quality.md → Negative Cases](judges/response_quality.md#-negative-cases) |

---


## **📂 Test Categories**


### 👤 **Customer Chatbot**

| Category | Description |
|----------|-------------|
| `browse_products` | Product search and listing |
| `check_price_stock` | Price and availability queries |
| `place_order` | Order placement flow |
| `order_history` | View past orders |
| `negative` | Unauthorized actions |

### 💼 **Client Chatbot**

| Category | Description |
|----------|-------------|
| `analytics` | Business analytics queries |
| `visualizations` | Chart generation |
| `chat_history` | Customer conversation lookup |
| `customer_insights` | Customer data analysis |
| `negative` | Write operations, unauthorized |

---


## **🔧 DatasetLoader**

```python
loader = DatasetLoader()
test_cases = loader.load_dataset("data/eval_datasets/customer")
```

Recursively loads all `.yaml` files and returns `TestCase` objects.


