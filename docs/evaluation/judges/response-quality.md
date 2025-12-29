# ResponseQualityJudge

Evaluates response quality using LLM-as-Judge pattern.

## Expected Field

```yaml
expected_output:
  response_quality: "Wireless Bluetooth Headphones, 840"
```

The value contains key facts that should appear in the response.

## Skip Condition

Skips if `response_quality` key is missing from expected_output.

## Negative Case

```yaml
# Chatbot should NOT respond (e.g., should refuse)
expected_output:
  response_quality: "null"
```

## Sub-Scores

| Sub-Score | Description |
|-----------|-------------|
| `relevance` | Does the response address the user's question? |
| `faithfulness` | Is the response grounded in facts (no hallucination)? |

## Evaluation Process

1. Get response and execution steps
2. LLM evaluates:
   - Relevance to user question
   - Faithfulness to execution results
3. Overall score = average of sub-scores

## Example Results

### Positive Case (Pass)

```yaml
judge_results:
  response_quality:
    score: 0.85
    passed: true
    sub_scores:
      relevance:
        score: 0.9
        reasoning: "Response directly answers the price question"
      faithfulness:
        score: 0.8
        reasoning: "Price matches database query results"
```

### Negative Case (Pass)

```yaml
# expected: response_quality: "null"
judge_results:
  response_quality:
    score: 1.0
    passed: true
    reasoning: "Correctly did not generate response"
```

### Fail Case

```yaml
judge_results:
  response_quality:
    score: 0.4
    passed: false
    sub_scores:
      relevance:
        score: 0.6
        reasoning: "Response partially addresses the question"
      faithfulness:
        score: 0.2
        reasoning: "Response contains information not in execution steps"
```

## Configuration

```yaml
# configs/evaluation/customer.yaml
response_quality_judge:
  enabled: true
  model: "gpt-4o"
  temperature: 0.0
  max_tokens: 16384
  prompt:
    name: "evaluation_evaluation_response_quality_judge"
    label: "latest"
```

## Prompt Template

The judge uses a Langfuse prompt with variables:
- `context` - Chatbot context
- `question` - User question
- `response` - Chatbot response
- `steps` - Execution steps
- `expected` - Expected facts in response
