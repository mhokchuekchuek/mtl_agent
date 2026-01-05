# SQLTool Base Class

Base class for all SQL query tools.

## Location

[`src/modules/tools/knowledge_retrieval/sql/base/main.py`](../../../../../../../src/modules/tools/knowledge_retrieval/sql/base/main.py)

## Class: SQLTool

Inherits from `langchain.tools.BaseTool`.

### Purpose

Uses LLM to generate SQL queries from natural language, validates them for security, and executes against the database.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sql_client` | BaseSQLDatabase | Database client |
| `llm_client` | BaseLLM | LLM client for SQL generation |
| `prompt_manager` | BasePromptManager | Prompt manager |
| `prompt_name` | str | Prompt name (default: "sql_generate") |
| `prompt_label` | str | Prompt version label (optional) |
| `allow_write` | bool | Allow write operations (default: False) |

### Input Schema

| Field | Type | Description |
|-------|------|-------------|
| `question` | str | Natural language question |
| `context` | dict | Additional context (optional) |

### Key Methods

| Method | Description |
|--------|-------------|
| `_run(question, context)` | Execute natural language query |
| `_get_schema_text()` | Get database schema for LLM context |
| `_get_base_variables()` | Get base prompt variables (schema, db_type) |
| `_generate_sql(**kwargs)` | Generate SQL from prompt + variables |
| `_is_write_query(sql)` | Check if SQL is INSERT/UPDATE/DELETE |

### Extension Points

Subclasses can:
- Override `_get_schema_text()` to filter tables
- Call `_generate_sql(**kwargs)` with extra variables (e.g., customer_id)
- Use `_get_base_variables()` to get schema and db_type automatically

### Usage

```python
from src.modules.tools.knowledge_retrieval.sql.base.main import SQLTool

# Read-only tool
sql_tool = SQLTool(
    sql_client=sql_client,
    llm_client=llm_client,
    prompt_manager=prompt_manager,
)

# Read-write tool
sql_tool_rw = SQLTool(
    sql_client=sql_client,
    llm_client=llm_client,
    prompt_manager=prompt_manager,
    allow_write=True,
)

# Execute query
result = sql_tool._run("What products are in stock?")
# Returns: {"sql": "SELECT ...", "results": [...]}
```

### Return Format

For SELECT queries:
```python
{"sql": "SELECT ...", "results": [{"col1": "val1", ...}, ...]}
```

For write queries:
```python
{"sql": "INSERT ...", "rows_affected": 1, "results": []}
```
