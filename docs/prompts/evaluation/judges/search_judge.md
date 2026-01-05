# **🔍 Search Judge Prompt**

LLM-as-Judge prompt for evaluating vector search quality.


---


## **🏷️ Langfuse Name**

`evaluation_judges_search_judge`


---


## **📍 Location**

[`prompts/evaluation/judges/search_judge.prompt`](../../../prompts/evaluation/judges/search_judge.prompt)


---


## **🔗 Used By**

- [SearchJudge](../../../evaluation/judges/search.md)


---


## **🤖 Model**

`gpt-4o`


---


## **📥 Variables**

| Variable | Type | Description |
|----------|------|-------------|
| `question` | string | User's original question |
| `expected_results` | list | Products that should be found |
| `steps` | list | Agent execution steps |


---


## **💡 Purpose**

Extract and evaluate search results:
1. Find `product_search` or `similar_products` tool calls in steps
2. Score relevance (are results relevant to query?)
3. Score coverage (are expected products found?)


---


## **📤 Output Schema**

```json
{
  "extracted_results": ["product1", "product2"],
  "relevance": {
    "score": 0.0-1.0,
    "reasoning": "..."
  },
  "coverage": {
    "score": 0.0-1.0,
    "reasoning": "..."
  }
}
```
