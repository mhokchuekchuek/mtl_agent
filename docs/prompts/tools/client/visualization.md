# **📈 Visualization Prompt**

Generate Plotly chart code.


---


## **📍 Location**

[`prompts/tools/client/visualization.prompt`](../../../prompts/tools/client/visualization.prompt)


---


## **🏷️ Prompt Name**

`tools_client_visualization`


---


## **💡 Purpose**

Generate Python code that creates Plotly charts from data.


---


## **📥 Input Variables**

| Variable | Description |
|----------|-------------|
| `columns` | Column names in data |
| `sample_data` | First 3 rows sample |
| `row_count` | Total rows |
| `request` | User's chart request |


---


## **📤 Output Format**

Python code with `fig` variable:

```python
import plotly.express as px

fig = px.bar(df, x='category', y='sales', title='Sales by Category')
```


---


## **📚 Available Libraries**

- `pd` - pandas
- `px` - plotly.express
- `go` - plotly.graph_objects
- `df` - DataFrame with data
- `data` - Raw data list


---


## **📊 Chart Types**

| Request | Chart |
|---------|-------|
| "bar chart of X by Y" | `px.bar()` |
| "pie chart" | `px.pie()` |
| "line chart over time" | `px.line()` |
| "scatter plot" | `px.scatter()` |


---


## **🔒 Sandbox Restrictions**

> ⚠️ **Important:** Code runs in restricted environment.

- No file I/O
- No network access
- No imports
- Limited builtins
