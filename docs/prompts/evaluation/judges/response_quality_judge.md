# **✨ Response Quality Judge Prompt**

LLM-as-Judge prompt for evaluating response quality.


---


## **🏷️ Langfuse Name**

`evaluation_judges_response_quality_judge`


---


## **📍 Location**

[`prompts/evaluation/judges/response_quality_judge.prompt`](../../../prompts/evaluation/judges/response_quality_judge.prompt)


---


## **🔗 Used By**

- [ResponseQualityJudge](../../../evaluation/judges/response_quality.md)


---


## **🤖 Model**

`gpt-4o`


---


## **📥 Variables**

| Variable | Type | Description |
|----------|------|-------------|
| `context` | string | Chatbot context (permissions, restrictions) |
| `question` | string | User's original question |
| `response` | string | Chatbot's response |
| `steps` | list | Agent execution steps |
| `expected` | string | Expected information in response |


---


## **💡 Purpose**

Evaluate response quality:
1. Score relevance (does response address the question?)
2. Score faithfulness (grounded in facts, no hallucination?)


---


## **📤 Output Schema**

```json
{
  "relevance": {
    "score": 0.0-1.0,
    "reasoning": "..."
  },
  "faithfulness": {
    "score": 0.0-1.0,
    "reasoning": "..."
  }
}
```
