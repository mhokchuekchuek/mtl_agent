# VisualizationJudge

Evaluates chart generation quality using LLM-as-Judge.

## Expected Fields

```yaml
expected_output:
  has_chart: true
  chart_type: "bar"
```

| Field | Values |
|-------|--------|
| `has_chart` | `true`, `false`, or `"null"` |
| `chart_type` | `"bar"`, `"line"`, `"pie"`, etc. |

## Skip Condition

Skips if both `has_chart` and `chart_type` are missing from expected_output.

## Negative Case

```yaml
# Chatbot should NOT create a chart
expected_output:
  has_chart: "null"
```

## Sub-Scores

| Sub-Score | Description |
|-----------|-------------|
| `appropriateness` | Is a chart appropriate for this query? |
| `chart_type` | Is the chart type suitable for the data? |

## Evaluation Process

1. Extract `create_visualization` and `create_chart` tool calls
2. For negative case: check no visualization was created
3. For positive case: LLM evaluates appropriateness and chart type
4. Overall score = average of sub-scores

## Example Results

### Positive Case (Pass)

```yaml
# expected: has_chart: true, chart_type: "bar"
judge_results:
  visualization:
    score: 0.9
    passed: true
    sub_scores:
      appropriateness:
        score: 1.0
        reasoning: "Bar chart is appropriate for category comparison"
      chart_type:
        score: 0.8
        reasoning: "Bar chart matches expected type"
```

### Negative Case (Pass)

```yaml
# expected: has_chart: "null"
judge_results:
  visualization:
    score: 1.0
    passed: true
    reasoning: "Correctly did not create visualization"
```

### No Chart Expected (Pass)

```yaml
# expected: has_chart: false
judge_results:
  visualization:
    score: 1.0
    passed: true
    sub_scores:
      appropriateness:
        score: 1.0
        reasoning: "Correctly determined chart not needed for single value query"
```

## Configuration

```yaml
# configs/evaluation/client.yaml
visualization_judge:
  enabled: true
  model: "gpt-4o"
  temperature: 0.0
  max_tokens: 16384
  prompt:
    name: "evaluation_evaluation_visualization_judge"
    label: "latest"
```

## Prompt Template

The judge uses a Langfuse prompt with variables:
- `question` - User question
- `response` - Chatbot response
- `steps` - Extracted visualization tool calls
- `expected_has_chart` - Whether chart expected
- `expected_chart_type` - Expected chart type
