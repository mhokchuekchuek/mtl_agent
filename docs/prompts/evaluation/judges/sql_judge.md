# **🗄️ SQL Judge Prompt**

Evaluate SQL query correctness.


---


## **📍 Location**

[`prompts/evaluation/judges/sql_judge.prompt`](../../../prompts/evaluation/judges/sql_judge.prompt)


---


## **🏷️ Prompt Name**

`evaluation_sql_judge`


---


## **💡 Purpose**

Judge whether the chatbot's SQL operations correctly answer the user's question.


---


## **📥 Input Variables**

| Variable | Description |
|----------|-------------|
| `current_date` | Current date for context |
| `context` | Chatbot context (client/customer) |
| `schema` | Database schema |
| `question` | User's original question |
| `expected_sql` | Reference SQL (single or list) |
| `expected_result` | Expected query result |
| `sql_operations` | Actual SQL operations executed |


---


## **📤 Output Format**

```json
{
  "result_match": {
    "score": 0.0-1.0,
    "reasoning": "Do the operations correctly fulfill the request?"
  },
  "efficiency": {
    "score": 0.0-1.0,
    "reasoning": "Is the SQL efficient?"
  }
}
```


---


## **📊 Scoring Criteria**


### ✅ **result_match**

| Score | Meaning |
|-------|---------|
| 1.0 | Results exactly match expected |
| 0.7+ | Results correct, minor differences |
| 0.5 | Partial match |
| 0.0 | Wrong results |


### ⚡ **efficiency**

| Score | Meaning |
|-------|---------|
| 1.0 | Optimal query |
| 0.7+ | Acceptable, minor inefficiencies |
| 0.5 | Unnecessary JOINs or subqueries |
| 0.0 | Very inefficient |


---


## **📝 Key Rules**

- Focus on **results**, not exact SQL syntax
- Hardcoded dates that produce correct results are acceptable
- For INSERT/UPDATE: verify operations executed correctly
- For SELECT: compare expected_result with actual
