# **🗄️ SQL Judge**

Evaluates SQL query correctness.


---


## **📍 Location**

[`evaluation/judges/sql/main.py`](../../../evaluation/judges/sql/main.py)


---


## **📋 Expected Field**

```yaml
expected_output:
  sql: "SELECT * FROM products WHERE category = 'Electronics'"
```


---


## **📊 Scoring**

| Sub-score | Weight | Description |
|-----------|--------|-------------|
| Result Match | 70% | Do agent results match expected results? |
| Efficiency | 30% | Is the SQL efficient? |

**Pass threshold**: 0.7


---


## **🔄 Flow**

<details>
<summary>📊 Flow</summary>

![Flow](../../assets/diagrams/evaluation/judges_sql_1.png)

</details>


---


## **❌ Negative Case**

```yaml
expected_output:
  sql: "null"
```

- Pass: No SQL operations found
- Fail: SQL was generated


---


## **📝 Prompt**

- [sql_judge.md](../../prompts/evaluation/judges/sql_judge.md) - Judge SQL correctness
- [sql_extractor.md](../../prompts/evaluation/extractors/sql_extractor.md) - Extract SQL from steps


---


## **🔗 References**

- [Decision: LLM-as-Judge](../../decisions/why_llm_as_judge.md)
