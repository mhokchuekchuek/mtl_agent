# SQL Tool

Generates and executes SQL queries from natural language questions.

## Location

`src/modules/tools/knowledge_retrieval/sql/`

## Architecture

```
User Question
      |
      v
+---------------------+
|  LLM generates SQL  |
|  (with schema)      |
+----------+----------+
           |
           v
+---------------------+
|  Validate SQL       |
|  (security check)   |
+----------+----------+
           |
           v
+---------------------+
|  Execute SQL        |
+---------------------+
           |
           v
      Results
```

## Components

### SQLTool

LangChain tool for natural language to SQL queries.

**Location**: `main.py`

**Inherits**: `langchain.tools.BaseTool`

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `sql_client` | BaseSQLDatabase | Database client |
| `llm_client` | BaseLLM | LLM client for SQL generation |
| `prompt_manager` | BasePromptManager | Prompt manager |
| `prompt_name` | str | Prompt name (default: "sql_generate") |
| `allow_write` | bool | Allow write operations (default: False) |

**Input Schema**:

| Field | Type | Description |
|-------|------|-------------|
| `question` | str | Natural language question |
| `context` | dict | Additional context (optional) |

**Methods**:

| Method | Description |
|--------|-------------|
| `_run(question, context)` | Execute natural language query |

### SQLValidator

SQL security validation.

**Location**: `validator.py`

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `allow_union` | bool | Allow UNION SELECT (default: False) |
| `allow_write` | bool | Allow write operations (default: False) |

**Always Blocked**:
- DDL: DROP, ALTER, CREATE, TRUNCATE
- Permissions: GRANT, REVOKE
- Execution: EXEC, EXECUTE, ATTACH, DETACH
- Patterns: Multiple statements (`;`), comments (`--`, `/*`)

**Blocked when `allow_write=False`**:
- DML: INSERT, UPDATE, DELETE, REPLACE

## Usage

```python
from libs.database.sql.sqlite.main import SQLiteClient
from libs.llm.client.litellm.main import LLMClient
from libs.llm.prompt_manager.langfuse.main import LangfusePromptManager
from src.modules.tools.knowledge_retrieval.sql.main import SQLTool

# Initialize clients
sql_client = SQLiteClient(db_path='data/erp.db')
llm_client = LLMClient(
    proxy_url='http://localhost:4000',
    api_key='sk-1234',
)
prompt_manager = LangfusePromptManager()

# Create read-only tool (default)
sql_tool = SQLTool(
    sql_client=sql_client,
    llm_client=llm_client,
    prompt_manager=prompt_manager,
)

# Create read-write tool
sql_tool_rw = SQLTool(
    sql_client=sql_client,
    llm_client=llm_client,
    prompt_manager=prompt_manager,
    allow_write=True,
)

# Query using _run method
results = sql_tool._run("What products are in stock?")
results = sql_tool._run(
    "Find products under $100",
    context={"category": "Electronics"}
)

# Write operations (only with allow_write=True)
result = sql_tool_rw._run("Create order for customer 1 with product 5")
# Returns: {"rows_affected": 1, "sql": "INSERT INTO ..."}

# Or use with LangChain agent
from langchain.agents import create_tool_calling_agent
tools = [sql_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
```

## Prompt

**Location**: `prompts/customer_chatbot/sql_generate.prompt`

The prompt provides:
- Database schema
- SQL generation rules (SELECT only)
- Output format (JSON with sql and explanation)

## Database Schema

```
Products(product_id PK, product_name, product_type, category, price)
Inventory(product_id, color, quantity, warehouse_id)
Warehouses(warehouse_id PK, warehouse_name, location)
Orders(order_id PK, order_date, customer_id, total_amount)
OrderDetails(order_detail_id PK, order_id, product_id, color, quantity, price)
Customers(customer_id PK, customer_name, email, phone_number, address)
```
