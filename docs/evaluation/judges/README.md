# Judges

Judges evaluate chatbot responses using LLM-as-Judge pattern.

## Available Judges

| Judge | Expected Field | Description |
|-------|----------------|-------------|
| [SQLJudge](sql.md) | `sql` | SQL query correctness |
| [SearchJudge](search.md) | `search_results` | Vector search quality |
| [ResponseQualityJudge](response-quality.md) | `response_quality` | Response relevance and faithfulness |
| [VisualizationJudge](visualization.md) | `has_chart`, `chart_type` | Chart generation quality |

## Skip Logic

Judges automatically skip if their expected field is missing:

```yaml
expected_output:
  response_quality: "100 products"
  # sql key missing = SQLJudge skips (returns None)
  # search_results key missing = SearchJudge skips
```

## Negative Cases

Use `"null"` string to test that chatbot should NOT perform an action:

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

## Return Type

All judges return `JudgeResult | None`:

```python
@dataclass
class JudgeResult:
    score: float          # 0.0 to 1.0
    passed: bool          # score >= threshold
    reasoning: str        # Human-readable explanation
    metadata: dict        # Sub-scores and details
```

- Returns `JudgeResult` - evaluated
- Returns `None` - skipped (no expected field)

## Sub-Scores

Each judge has specific sub-scores in `metadata`:

| Judge | Sub-Scores |
|-------|------------|
| SQLJudge | `syntax`, `correctness` |
| SearchJudge | `relevance`, `coverage` |
| ResponseQualityJudge | `relevance`, `faithfulness` |
| VisualizationJudge | `appropriateness`, `chart_type` |

## Pass Threshold

Default pass threshold is `0.7` (configurable in config YAML).
