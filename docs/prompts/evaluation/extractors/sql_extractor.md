# **🔧 SQL Extractor Prompt**

Extraction prompt for pulling SQL operations from agent steps.


---


## **🏷️ Langfuse Name**

`evaluation_extractors_sql_extractor`


---


## **📍 Location**

[`prompts/evaluation/extractors/sql_extractor.prompt`](../../../../prompts/evaluation/extractors/sql_extractor.prompt)


---


## **🔗 Used By**

- [SQLJudge](../../../evaluation/judges/sql.md)


---


## **🤖 Model**

`gpt-4o-mini`


---


## **📥 Variables**

| Variable | Type | Description |
|----------|------|-------------|
| `question` | string | User's original question |
| `steps` | list | Agent execution steps |


---


## **💡 Purpose**

Extract all SQL queries and results from execution steps:
1. Find SQL-related tool calls in steps
2. Extract the SQL query executed
3. Extract the query result or outcome


---


## **📤 Output Schema**

```json
{
  "sql_operations": [
    {
      "tool_name": "analytics_query",
      "sql": "SELECT * FROM products",
      "result": "[{...}]"
    }
  ]
}
```

> 📝 **Note:** Returns empty array if no SQL operations found.
