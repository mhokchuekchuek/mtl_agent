# SQLJudge

Evaluates SQL query correctness using LLM-as-Judge.

## Expected Field

```yaml
expected_output:
  sql: "SELECT COUNT(*) FROM Products"
```

## Skip Condition

Skips if `sql` key is missing from expected_output.

## Negative Case

```yaml
# Chatbot should NOT generate SQL
expected_output:
  sql: "null"
```

## Sub-Scores

| Sub-Score | Description |
|-----------|-------------|
| `syntax` | Is the SQL syntactically correct? |
| `correctness` | Does it match the expected SQL logic/intent? |

## Evaluation Process

1. Extract `sql_query` tool calls from execution steps
2. LLM evaluates:
   - Syntax validity
   - Semantic correctness compared to expected SQL
3. Overall score = average of sub-scores

## Example Results

### Positive Case (Pass)

```yaml
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
        reasoning: "Query returns correct result but uses different join style"
```

### Negative Case (Pass)

```yaml
# expected: sql: "null"
judge_results:
  sql:
    score: 1.0
    passed: true
    reasoning: "Correctly refused to generate SQL"
```

### Negative Case (Fail)

```yaml
# expected: sql: "null", but chatbot generated SQL
judge_results:
  sql:
    score: 0.0
    passed: false
    reasoning: "Should not generate SQL but generated: SELECT * FROM Customers"
```

## Configuration

```yaml
# configs/evaluation/customer.yaml
sql_judge:
  enabled: true
  model: "gpt-4o"
  temperature: 0.0
  max_tokens: 16384
  prompt:
    name: "evaluation_evaluation_sql_judge"
    label: "latest"
```

## Prompt Template

The judge uses a Langfuse prompt with variables:
- `context` - Chatbot context (permissions, restrictions)
- `schema` - Database schema
- `question` - User question
- `expected_sql` - Expected SQL query
- `steps` - Extracted sql_query tool calls
