# SearchJudge

Evaluates vector search quality using LLM-as-Judge.

## Expected Field

```yaml
expected_output:
  search_results: ["Wireless Bluetooth Headphones", "Noise Cancelling Headphones"]
```

## Skip Condition

Skips if `search_results` key is missing from expected_output.

## Negative Case

```yaml
# Chatbot should NOT perform search
expected_output:
  search_results: "null"
```

## Empty Results Case

```yaml
# Search should return no results
expected_output:
  search_results: []
```

## Sub-Scores

| Sub-Score | Description |
|-----------|-------------|
| `relevance` | Are results relevant to the query? |
| `coverage` | Are expected products found in results? |

## Evaluation Process

1. Extract `product_search` and `similar_products` tool calls
2. LLM evaluates:
   - Relevance of returned products
   - Coverage of expected products
3. Overall score = average of sub-scores

## Example Results

### Positive Case (Pass)

```yaml
judge_results:
  search:
    score: 0.85
    passed: true
    sub_scores:
      relevance:
        score: 0.9
        reasoning: "All results are headphone products"
      coverage:
        score: 0.8
        reasoning: "Found 2 of 3 expected products"
```

### Negative Case (Pass)

```yaml
# expected: search_results: "null"
judge_results:
  search:
    score: 1.0
    passed: true
    reasoning: "Correctly did not perform search"
```

### Empty Results Case (Pass)

```yaml
# expected: search_results: []
judge_results:
  search:
    score: 1.0
    passed: true
    reasoning: "Correctly returned no results"
```

## Configuration

```yaml
# configs/evaluation/customer.yaml
search_judge:
  enabled: true
  model: "gpt-4o"
  temperature: 0.0
  max_tokens: 16384
  prompt:
    name: "evaluation_evaluation_search_judge"
    label: "latest"
```

## Prompt Template

The judge uses a Langfuse prompt with variables:
- `question` - User question
- `expected_results` - Expected product names
- `steps` - Extracted search tool calls
