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


## **🔄 How It Works**

1. **Extract SQL** - Use LLM extractor to get SQL from agent's execution steps
2. **Run Expected SQL** - Execute `expected_output.sql` against real database → get expected result
3. **Compare** - LLM compares agent's SQL operations with expected result
4. **Score** - Return result_match (70%) + efficiency (30%)

<details>
<summary>📊 Flow Diagram</summary>

![Flow](../../assets/diagrams/evaluation/judges_sql_1.png)

</details>


---


## **📥 Multiple SQL Statements**

For operations with multiple SQL statements (e.g., place order):

```yaml
expected_output:
  sql:
    - "SELECT product_id, price FROM Products WHERE product_id = 10"
    - "INSERT INTO Orders (customer_id, total_amount) VALUES (1, 279)"
```

Each statement is executed sequentially.


---


## **❌ Negative Case**

```yaml
expected_output:
  sql: "null"
```

- Pass: No SQL operations found
- Fail: SQL was generated


---


## **📝 Prompts**

| Prompt | Purpose |
|--------|---------|
| [sql_extractor.md](../../prompts/evaluation/extractors/sql_extractor.md) | Extract SQL from agent steps |
| [sql_judge.md](../../prompts/evaluation/judges/sql_judge.md) | Judge SQL correctness |


---


## **🔗 References**

- [Decision: LLM-as-Judge](../../decisions/why_llm_as_judge.md)
