# **⚖️ Judges**

LLM-as-Judge implementations for evaluating chatbot responses.


---


## **📋 Overview**

All judges follow the same pattern:
1. Check if expected field exists (skip if not)
2. Handle negative cases (expected: "null")
3. Extract relevant data from agent steps
4. Send to LLM for evaluation
5. Return score with sub-scores and reasoning


---


## **🔍 Judges**

| Judge | Expected Field | Sub-scores | Link |
|-------|----------------|------------|------|
| SQL | `sql` | result_match, efficiency | [sql.md](sql.md) |
| Search | `search_results` | relevance, coverage | [search.md](search.md) |
| Visualization | `has_chart`, `chart_type` | appropriateness, chart_type | [visualization.md](visualization.md) |
| Response Quality | `response_quality` | relevance, faithfulness | [response_quality.md](response_quality.md) |


---


## **🔧 Base Class**

All judges extend `BaseJudge`:

```python
class BaseJudge(ABC):
    name: str = "base_judge"
    strategy: EvaluationStrategy = EvaluationStrategy.FINAL_RESPONSE

    @abstractmethod
    def evaluate(
        self,
        input_data: dict,
        output_data: dict,
        expected: dict | None = None,
    ) -> JudgeResult | None:
        pass
```


---


## **📊 JudgeResult**

```python
@dataclass
class JudgeResult:
    score: float        # 0.0 - 1.0
    passed: bool        # score >= threshold
    reasoning: str      # Human-readable explanation
    metadata: dict      # Sub-scores, extracted values
```


---


## **🎯 Evaluation Strategy**

| Strategy | Description |
|----------|-------------|
| `FINAL_RESPONSE` | Evaluate final response only |
| `SINGLE_STEP` | Evaluate specific tool execution |
| `TRAJECTORY` | Evaluate entire execution path |


---


## **❌ Negative Cases**

For testing that the agent correctly refuses or skips actions:

| Expected Value | Meaning |
|----------------|---------|
| `sql: "null"` | Should not generate SQL |
| `search_results: []` | Should return no results |
| `has_chart: false` | Should not create chart |
| `response_quality: "null"` | Should not respond |


---


## **✅ Pass Thresholds**

| Judge | Threshold |
|-------|-----------|
| SQL | 0.7 |
| Search | 0.6 |
| Visualization | 0.7 |
| Response Quality | 0.7 |



