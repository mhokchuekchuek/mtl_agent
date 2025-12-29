# Adding Tests

## Adding a Test Case

### 1. Choose the Right Location

```
evaluation/datasets/{chatbot}/{judge_type}/{turn_type}/
```

- `chatbot`: `customer` or `client`
- `judge_type`: `sql`, `search`, `response_quality`, `visualization`
- `turn_type`: `single_turn`, `multi_turn`, or `negative`

### 2. Add to Existing YAML or Create New

```yaml
# evaluation/datasets/customer/sql/single_turn/aggregation.yaml

test_cases:
  # Add new test case here
  - id: sum_all_prices
    input:
      question: "What is the total value of all products?"
    expected_output:
      sql: "SELECT SUM(price) FROM Products"
```

### 3. Test Case ID Rules

- Use snake_case
- Be descriptive: `count_products_by_category`
- Unique within the dataset

### 4. Run Evaluation

```bash
python scripts/run_eval.py customer
```

## Adding a New Judge

### 1. Create Judge Class

```python
# evaluation/judges/my_judge/main.py

from evaluation.entities import JudgeResult
from evaluation.judges.base import BaseJudge

class MyJudge(BaseJudge):
    name = "my_judge"
    
    def evaluate(
        self,
        input_data: dict,
        output_data: dict,
        expected: dict | None = None,
        context: dict | None = None,
    ) -> JudgeResult | None:
        # Skip if no expected field
        if expected is None or "my_field" not in expected:
            return None
        
        expected_value = expected.get("my_field")
        is_negative_case = expected_value == "null"
        
        # Evaluate...
        
        return JudgeResult(
            score=score,
            passed=score >= 0.7,
            reasoning="...",
            metadata={...},
        )
```

### 2. Register in Selector

```python
# evaluation/judges/selector.py

class JudgeSelector(BaseToolSelector):
    _PROVIDERS = {
        "sql": "evaluation.judges.sql.main.SQLJudge",
        "search": "evaluation.judges.search.main.SearchJudge",
        "my_judge": "evaluation.judges.my_judge.main.MyJudge",  # Add here
    }
```

### 3. Add Config

```yaml
# configs/evaluation/customer.yaml

my_judge:
  enabled: true
  model: "gpt-4o"
  temperature: 0.0
  max_tokens: 16384
  prompt:
    name: "evaluation_my_judge"
    label: "latest"
```

### 4. Add to Dependencies

```python
# evaluation/dependencies/customer.py

# In build_evaluation_service()
my_cfg = getattr(eval_config, "my_judge", None)
if my_cfg and getattr(my_cfg, "enabled", False):
    judge = JudgeSelector.create(
        provider="my_judge",
        llm_client=llm_client,
        prompt_manager=prompt_manager,
        # ... other params
    )
    judges.append(judge)
```

### 5. Create Prompt in Langfuse

Create prompt `evaluation_my_judge` with appropriate template.

### 6. Add Test Cases

```yaml
# evaluation/datasets/customer/my_judge/single_turn/basic.yaml

test_cases:
  - id: test_my_feature
    input:
      question: "..."
    expected_output:
      my_field: "expected value"
```

## Best Practices

1. **Test both positive and negative cases**
2. **Use specific expected values** - avoid vague expectations
3. **Test edge cases** - empty results, errors, boundary conditions
4. **Keep test cases independent** - each should work standalone
5. **Document unusual test cases** - add comments in YAML if needed
