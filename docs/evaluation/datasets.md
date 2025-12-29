# Datasets

Test cases are stored as YAML files in `evaluation/datasets/`.

## Directory Structure

```
evaluation/datasets/
├── customer/
│   ├── sql/
│   │   ├── single_turn/
│   │   ├── multi_turn/
│   │   └── negative/
│   ├── search/
│   │   ├── single_turn/
│   │   ├── multi_turn/
│   │   └── negative/
│   └── response_quality/
│       ├── single_turn/
│       └── multi_turn/
└── client/
    ├── sql/
    ├── visualization/
    └── response_quality/
```

## YAML Format

### Single-Turn Test Case

```yaml
name: sql_aggregation
description: Test COUNT, SUM, AVG queries

test_cases:
  - id: count_all_products
    input:
      question: "How many products do you have?"
    expected_output:
      sql: "SELECT COUNT(*) FROM Products"

  - id: product_info
    input:
      question: "Tell me about Wireless Bluetooth Headphones"
    expected_output:
      response_quality: "Wireless Bluetooth Headphones, 840"
```

### Multi-Turn Test Case

```yaml
name: search_multi_turn
description: Multi-turn product search

test_cases:
  - id: refine_search
    turns:
      - input:
          question: "I need headphones"
        expected_output:
          search_results: ["Wireless Bluetooth Headphones", "Noise Cancelling Headphones"]
      - input:
          question: "Which one has noise cancelling?"
        expected_output:
          response_quality: "Noise Cancelling Headphones"
```

## Expected Output Fields

| Field | Judge | Description |
|-------|-------|-------------|
| `sql` | SQLJudge | Expected SQL query |
| `search_results` | SearchJudge | Expected product names in results |
| `response_quality` | ResponseQualityJudge | Key facts expected in response |
| `has_chart` | VisualizationJudge | Whether chart should be generated |
| `chart_type` | VisualizationJudge | Expected chart type (bar, line, pie) |

## Skip vs Negative Cases

### Skip (Judge not evaluated)
No key in expected_output = judge skips this test case

```yaml
expected_output:
  response_quality: "100 products"
  # sql key missing = SQLJudge skips
```

### Negative Case (Should NOT do something)
Use `"null"` string value = judge checks that action was NOT taken

```yaml
# Should NOT generate SQL
expected_output:
  sql: "null"

# Should NOT perform search
expected_output:
  search_results: "null"

# Should NOT create chart
expected_output:
  has_chart: "null"
```

### Empty Results (Search only)
Use empty array `[]` = search should return no results

```yaml
expected_output:
  search_results: []
```

## Folder Categories

| Folder | Description |
|--------|-------------|
| `single_turn/` | One question, one response |
| `multi_turn/` | Conversation with multiple exchanges |
| `negative/` | Cases where chatbot should refuse/not act |
