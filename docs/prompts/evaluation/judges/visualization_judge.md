# **📊 Visualization Judge Prompt**

LLM-as-Judge prompt for evaluating chart generation.


---


## **🏷️ Langfuse Name**

`evaluation_judges_visualization_judge`


---


## **📍 Location**

[`prompts/evaluation/judges/visualization_judge.prompt`](../../../prompts/evaluation/judges/visualization_judge.prompt)


---


## **🔗 Used By**

- [VisualizationJudge](../../../evaluation/judges/visualization.md)


---


## **🤖 Model**

`gpt-4o`


---


## **📥 Variables**

| Variable | Type | Description |
|----------|------|-------------|
| `question` | string | User's original question |
| `response` | string | Chatbot's response |
| `steps` | list | Agent execution steps |
| `expected_has_chart` | boolean | Should chart be generated? |
| `expected_chart_type` | string | Expected chart type |


---


## **💡 Purpose**

Extract and evaluate visualization decisions:
1. Find `create_visualization` tool calls in steps
2. Score appropriateness (right decision to generate/not generate?)
3. Score chart type (suitable for the data?)


---


## **📤 Output Schema**

```json
{
  "extracted_has_chart": true,
  "extracted_chart_type": "bar",
  "appropriateness": {
    "score": 0.0-1.0,
    "reasoning": "..."
  },
  "chart_type": {
    "score": 0.0-1.0,
    "reasoning": "..."
  }
}
```
