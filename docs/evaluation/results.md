# **📊 Results Format**

Evaluation results are saved to `results/{chatbot}/{category}/{test_id}/`.


---


## **📁 Directory Structure**

```
results/
├── customer/
│   ├── browse_products/
│   │   └── single_turn/
│   │       └── search_wireless_headphones/
│   │           ├── results.yaml
│   │           └── detail.yaml
│   ├── place_order/
│   │   └── multi_turn/
│   │       └── place_order_flow/
│   │           ├── results.yaml
│   │           └── detail.yaml
│   └── negative/
│       └── single_turn/
│           └── refuse_unauthorized/
│               ├── results.yaml
│               └── detail.yaml
└── client/
    └── ...
```

---


## **📄 results.yaml**

Summary file with scores and truncated output.


### 1️⃣ **Single-Turn**

```yaml
test_id: search_wireless_headphones
type: single_turn
passed: true
overall_score: 0.85
latency_ms: 5234
timestamp: '2025-12-29T17:30:00'

input:
  question: "I'm looking for wireless headphones"

output:
  response: "Here are some wireless headphones..."  # truncated

expected:
  search_results: ["Wireless Bluetooth Headphones", "Noise Cancelling Headphones"]

judge_results:
  search:
    score: 0.85
    passed: true
    expected:
      results: ["Wireless Bluetooth Headphones", "Noise Cancelling Headphones"]
    actual:
      results: ["Wireless Bluetooth Headphones", "Noise Cancelling Headphones"]
    sub_scores:
      relevance:
        score: 0.9
        reasoning: "Results are relevant to query"
      coverage:
        score: 0.8
        reasoning: "All expected products found"
```

### 🔄 **Multi-Turn**

```yaml
test_id: place_order_flow
type: multi_turn
passed: true
overall_score: 0.73
total_latency_ms: 23347
timestamp: '2025-12-29T17:35:00'

turns:
  - turn: 0
    input:
      question: "I want to order headphones"
    output:
      response: "Here are some headphones options..."
    expected:
      search_results: ["Wireless Bluetooth Headphones"]
    latency_ms: 15000
    judge_results:
      search:
        score: 0.9
        passed: true

  - turn: 1
    input:
      question: "Order the first one"
    output:
      response: "Order placed successfully..."
    expected:
      sql: "INSERT INTO orders..."
    latency_ms: 8347
    judge_results:
      sql:
        score: 0.75
        passed: true
```

---


## **📋 detail.yaml**

Full execution data for debugging.


### 1️⃣ **Single-Turn**

```yaml
output:
  response: "Full response without truncation..."
  steps:
    - name: translation_agent
      input:
        query: "I'm looking for wireless headphones"
      output:
        translated_query: "I'm looking for wireless headphones"
        detected_lang: "en"
    - name: product_agent
      input:
        query: "I'm looking for wireless headphones"
      output:
        response: "Here are some wireless headphones..."
      tool_calls:
        - name: product_search
          input:
            query: "wireless headphones"
          output:
            results: [...]
```

### 🔄 **Multi-Turn**

```yaml
turns:
  - turn: 0
    output:
      response: "Full response..."
      steps: [...]

  - turn: 1
    output:
      response: "Full response..."
      steps: [...]
```

---


## **📈 Summary CSV**

`summary.csv` is generated with aggregated scores:

| Column | Description |
|--------|-------------|
| test_id | Test case ID |
| turn_type | single_turn, multi_turn, negative |
| passed | true/false |
| overall_score | Average of all judge scores |
| latency_ms | Total latency |
| {judge}_score | Score per judge |

---


## **📊 Score Interpretation**

| Score | Meaning |
|-------|---------|
| 1.0 | Perfect |
| 0.7+ | Passed (default threshold) |
| 0.5-0.7 | Partial match |
| < 0.5 | Failed |
