# SQL Judge

Evaluates SQL query correctness.

## Expected Field

```yaml
expected_output:
  sql: "SELECT * FROM products WHERE category = 'Electronics'"
```

## Scoring

| Sub-score | Weight | Description |
|-----------|--------|-------------|
| Result Match | 70% | Do agent results match expected results? |
| Efficiency | 30% | Is the SQL efficient? |

**Pass threshold**: 0.7

## Flow

```mermaid
flowchart TD
    subgraph Extract
        STEPS[Agent Steps] --> EXT[LLM Extractor]
        EXT --> OPS[SQL Operations + Results]
    end
    
    subgraph Execute
        EXPSQL[Expected SQL] --> EXEC[Execute]
        EXEC --> EXPRES[Expected Results]
    end
    
    subgraph Judge
        OPS --> LLM[LLM Judge]
        EXPSQL --> LLM
        EXPRES --> LLM
        LLM --> SCORE[Score]
    end
```

## Negative Case

```yaml
expected_output:
  sql: "null"
```

- Pass: No SQL operations found
- Fail: SQL was generated

## Prompts

| Prompt | Purpose |
|--------|---------|
| `evaluation_extractors_sql_extractor` | Extract SQL from steps |
| `evaluation_judges_sql_judge` | Judge SQL correctness |

## References

- [SQLJudge](../../../evaluation/judges/sql/main.py)
- [Decision: Why SQL Judge](../../decisions/why_sql_judge.md)
