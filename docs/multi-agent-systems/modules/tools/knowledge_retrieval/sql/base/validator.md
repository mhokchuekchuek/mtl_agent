# SQL Validator

SQL security validation to prevent injection and unauthorized operations.

## Location

[`src/modules/tools/knowledge_retrieval/sql/base/validator.py`](../../../../../../../src/modules/tools/knowledge_retrieval/sql/base/validator.py)

## Class: SQLValidator

### Purpose

Validates SQL queries for security before execution.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allow_union` | bool | False | Allow UNION SELECT |
| `allow_write` | bool | False | Allow write operations |

### Blocked Operations

#### Always Blocked

| Category | Keywords |
|----------|----------|
| DDL | DROP, ALTER, CREATE, TRUNCATE |
| Permissions | GRANT, REVOKE |
| Execution | EXEC, EXECUTE, ATTACH, DETACH |
| Patterns | Multiple statements (`;`), comments (`--`, `/*`) |

#### Blocked when `allow_write=False`

| Category | Keywords |
|----------|----------|
| DML | INSERT, UPDATE, DELETE, REPLACE |

### Methods

| Method | Description |
|--------|-------------|
| `is_safe(sql)` | Returns True if SQL passes validation |
| `sanitize(sql)` | Attempts to clean SQL, returns None if unsafe |

### Usage

```python
from src.modules.tools.knowledge_retrieval.sql.base.validator import SQLValidator

# Read-only validator
validator = SQLValidator(allow_write=False)
validator.is_safe("SELECT * FROM products")  # True
validator.is_safe("DELETE FROM products")    # False

# Read-write validator
validator_rw = SQLValidator(allow_write=True)
validator_rw.is_safe("INSERT INTO orders ...")  # True
validator_rw.is_safe("DROP TABLE orders")       # False (always blocked)
```
