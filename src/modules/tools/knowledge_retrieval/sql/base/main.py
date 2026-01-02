"""SQL query tool for natural language to SQL query generation."""

import json
from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from .validator import SQLValidator

logger = get_logger(__name__)


class SQLQueryInput(BaseModel):
    """Input schema for SQL query tool."""

    question: str = Field(description="Natural language question about the database")
    context: Optional[dict] = Field(
        default=None, description="Additional context (e.g., product_ids)"
    )


class SQLTool(BaseTool):
    """Base class for SQL query tools.

    Uses LLM to generate SQL queries based on database schema,
    validates them for security, and executes them.

    Subclasses can:
    - Override `_get_schema_text()` to filter tables (e.g., ALLOWED_TABLES)
    - Call `_generate_sql(**kwargs)` with extra variables (e.g., customer_id)
    - Use `_get_base_variables()` to get schema and db_type automatically

    Example:
        class CustomerOrderSQLTool(SQLTool):
            def _run(self, question: str):
                sql = self._generate_sql(
                    question=question,
                    customer_id=self.customer_id,  # extra variable
                )
                ...
    """

    name: str = "sql_query"
    description: str = (
        "Query the database using natural language. "
        "Use this when you need to get product details, check inventory, "
        "or retrieve other structured data from the database."
    )
    args_schema: Type[BaseModel] = SQLQueryInput
    sql_client: Optional[BaseSQLDatabase] = None
    llm_client: Optional[BaseLLM] = None
    prompt_manager: Optional[BasePromptManager] = None
    prompt_name: str = "sql_generate"
    prompt_label: Optional[str] = None
    validator: Optional[SQLValidator] = None
    allow_write: bool = False

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "sql_generate",
        prompt_label: Optional[str] = None,
        allow_write: bool = False,
        **kwargs,
    ):
        """Initialize SQL tool.

        Args:
            sql_client: Database client for query execution.
            llm_client: LLM client for SQL generation.
            prompt_manager: Prompt manager for retrieving prompts.
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Prompt version label (e.g., "latest", "production").
            allow_write: Whether to allow write operations (INSERT, UPDATE, DELETE).
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.sql_client = sql_client
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label
        self.allow_write = allow_write
        self.validator = SQLValidator(allow_write=allow_write)

        # Update description if write is allowed
        if allow_write:
            self.description = (
                "Query or modify the database using natural language. "
                "Use this for reading data (SELECT), creating orders (INSERT), "
                "updating records (UPDATE), or deleting data (DELETE)."
            )

        logger.info(f"SQLTool initialized (allow_write={allow_write})")

    def _get_schema_text(self) -> str:
        """Get database schema as text for LLM context.

        Returns:
            Formatted schema string.
        """
        tables = self.sql_client.get_tables()
        schema_parts = []

        for table in tables:
            columns = self.sql_client.get_schema(table)
            col_defs = []
            for col in columns:
                pk = " PK" if col.get("primary_key") else ""
                nullable = "" if col.get("nullable") else " NOT NULL"
                col_defs.append(f"{col['name']} {col['type']}{pk}{nullable}")

            schema_parts.append(f"{table}({', '.join(col_defs)})")

        return "\n".join(schema_parts)

    def _get_base_variables(self) -> dict:
        """Get base variables that all SQL prompts need.

        Automatically provides:
        - schema: Database schema from _get_schema_text()
        - db_type: Database type (sqlite, postgresql) for dialect-specific SQL

        Subclasses can use this in custom _generate methods:
            variables = self._get_base_variables()
            variables.update({"customer_id": self.customer_id})

        Returns:
            Dict with schema and db_type.
        """
        return {
            "schema": self._get_schema_text(),
            "db_type": self.sql_client.get_db_type(),
        }

    def _generate_sql(self, **kwargs) -> str:
        """Generate SQL query from natural language using LLM.

        Merges base variables (schema, db_type) with provided kwargs,
        then compiles the prompt and generates SQL.

        Args:
            **kwargs: Variables to pass to prompt. Common ones:
                - question: Natural language question
                - customer_id: For customer-scoped queries
                - context: Additional context as JSON string

        Returns:
            Generated SQL query string.

        Raises:
            ValueError: If LLM response cannot be parsed as JSON.
        """
        # Get prompt from prompt manager
        prompt = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )

        # Merge base variables with kwargs
        variables = self._get_base_variables()
        variables.update(kwargs)

        # Compile prompt with variables
        compiled = prompt.compile(**variables)

        # Generate SQL using LLM
        response = self.llm_client.generate(prompt=compiled)

        # Parse JSON response
        try:
            result = json.loads(response)
            sql = result.get("sql", "")
            explanation = result.get("explanation", "")

            if explanation:
                logger.debug(f"SQL explanation: {explanation}")

            return sql

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {response}")
            raise ValueError(f"Invalid LLM response format: {e}")

    def _is_write_query(self, sql: str) -> bool:
        """Check if SQL is a write operation.

        Args:
            sql: SQL query string.

        Returns:
            True if query is INSERT, UPDATE, or DELETE.
        """
        normalized = sql.strip().upper()
        return any(normalized.startswith(kw) for kw in ["INSERT", "UPDATE", "DELETE"])

    def _run(
        self,
        question: str,
        context: Optional[dict] = None,
    ) -> list[dict] | dict:
        """Execute natural language query against database.

        Args:
            question: Natural language question.
            context: Additional context for query generation.

        Returns:
            For SELECT: List of result rows as dictionaries.
            For INSERT/UPDATE/DELETE: Dict with rows_affected count.

        Raises:
            ValueError: If generated SQL is invalid or unsafe.
        """
        logger.info(f"Processing question: {question}")

        # Generate SQL from question
        sql = self._generate_sql(
            question=question,
            context=json.dumps(context) if context else "",
        )
        logger.debug(f"Generated SQL: {sql}")

        # Validate SQL for security
        if not self.validator.is_safe(sql):
            # Try to sanitize
            sanitized = self.validator.sanitize(sql)
            if sanitized:
                logger.warning(f"SQL sanitized: {sql} -> {sanitized}")
                sql = sanitized
            else:
                raise ValueError(f"Generated SQL failed security validation: {sql}")

        # Execute query based on type
        if self._is_write_query(sql):
            rows_affected = self.sql_client.execute(sql)
            logger.info(f"Write query affected {rows_affected} rows")
            return {"sql": sql, "rows_affected": rows_affected, "results": []}
        else:
            results = self.sql_client.query(sql)
            logger.info(f"Query returned {len(results)} rows")
            return {"sql": sql, "results": results}
