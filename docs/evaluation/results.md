# Results Format

Evaluation results are saved to `results/{chatbot}/{turn_type}/{test_id}_{timestamp}/`.

## Directory Structure

```
results/
├── customer/
│   ├── single_turn/
│   │   └── count_all_products_20251229_173000/
│   │       ├── results.yaml
│   │       └── detail.yaml
│   ├── multi_turn/
│   │   └── product_price_inquiry_20251229_173500/
│   │       ├── results.yaml
│   │       └── detail.yaml
│   └── negative/
│       └── ...
└── client/
    └── ...
```

## results.yaml

Summary file with scores and truncated output.

### Single-Turn

```yaml
test_id: count_all_products
type: single_turn
passed: true
overall_score: 0.85
latency_ms: 5234
timestamp: '2025-12-29T17:30:00'

input:
  question: "How many products do you have?"

output:
  response: "We have 100 products in our catalog..."  # truncated to 200 chars

expected:
  sql: "SELECT COUNT(*) FROM Products"

judge_results:
  sql:
    score: 0.9
    passed: true
    sub_scores:
      syntax:
        score: 1.0
        reasoning: "Query is syntactically correct"
      correctness:
        score: 0.8
        reasoning: "Query returns correct result"
  response_quality:
    score: 0.8
    passed: true
    sub_scores:
      relevance:
        score: 0.9
        reasoning: "Response directly answers the question"
      faithfulness:
        score: 0.7
        reasoning: "Response grounded in execution results"
```

### Multi-Turn

```yaml
test_id: product_price_inquiry
type: multi_turn
passed: true
overall_score: 0.73
total_latency_ms: 23347
timestamp: '2025-12-29T17:35:00'

turns:
  - turn: 0
    input:
      question: "I want headphones"
    output:
      response: "Here are some headphones options..."
    expected:
      response_quality: "Wireless Bluetooth Headphones, Noise Cancelling Headphones"
    latency_ms: 15000
    judge_results:
      response_quality:
        score: 0.9
        passed: true
        sub_scores:
          relevance:
            score: 1.0
            reasoning: "..."
          faithfulness:
            score: 0.8
            reasoning: "..."

  - turn: 1
    input:
      question: "How much is the noise cancelling one?"
    output:
      response: "The Noise Cancelling Headphones costs $985..."
    expected:
      sql: "SELECT price FROM Products WHERE product_name = 'Noise Cancelling Headphones'"
    latency_ms: 8347
    judge_results:
      sql:
        score: 0.75
        passed: true
        sub_scores:
          syntax:
            score: 1.0
            reasoning: "..."
          correctness:
            score: 0.5
            reasoning: "..."
```

## detail.yaml

Full execution data for debugging.

### Single-Turn

```yaml
output:
  response: "Full response without truncation..."
  steps:
    - name: translation_agent
      input:
        user_input: "How many products do you have?"
        target_lang: "en"
      output:
        translated_text: "How many products do you have?"
        detected_lang: "en"
    - name: product_agent
      input:
        query: "How many products do you have?"
      output:
        response: "We have 100 products..."
      tool_calls:
        - name: sql_query
          input:
            question: "How many products are there?"
          output:
            sql: "SELECT COUNT(*) FROM Products"
            results: [{"COUNT(*)": 100}]
```

### Multi-Turn

```yaml
turns:
  - turn: 0
    output:
      response: "Full response..."
      steps:
        - name: translation_agent
          input: {...}
          output: {...}
        - name: product_agent
          input: {...}
          output: {...}
          tool_calls: [...]

  - turn: 1
    output:
      response: "Full response..."
      steps: [...]
```

## Score Interpretation

| Score | Meaning |
|-------|---------|
| 1.0 | Perfect |
| 0.7+ | Passed (default threshold) |
| 0.5-0.7 | Partial match |
| < 0.5 | Failed |
