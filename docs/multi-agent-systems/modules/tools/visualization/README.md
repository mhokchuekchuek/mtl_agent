# VisualizationTool

LangChain tool for creating Plotly visualizations using LLM-generated code.

## Location
`src/modules/tools/visualization/main.py`

## How It Works

1. Receives data (list of dicts) and visualization request (natural language)
2. Uses LLM to generate Plotly code based on data schema and request
3. Executes code in sandbox with limited globals
4. Returns Plotly chart as HTML string

## Usage

```python
from src.modules.tools.visualization.main import VisualizationTool

tool = VisualizationTool(
    llm_client=litellm_client,
    prompt_manager=prompt_manager,
    prompt_name="client_chatbot_visualization",
)

# In ReAct agent
result = tool._run(
    data=[{"category": "A", "value": 100}, {"category": "B", "value": 200}],
    request="Create a bar chart showing value by category"
)
# Returns: <div id="...">...</div> (Plotly HTML)
```

## Sandbox Execution

The tool executes LLM-generated code in a restricted environment:
- Allowed: `pd`, `px`, `go`, `df`, `data`, basic builtins
- Blocked: file I/O, network, imports, dangerous functions

## Prompt
Uses `client_chatbot_visualization` prompt to generate Plotly code.

## Error Handling
- Returns error message HTML if code generation or execution fails
- No retry - returns fallback error message
