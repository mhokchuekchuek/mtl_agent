"""Customer product SQL tool - Products and Inventory only."""

from typing import Optional, Type

from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from ..base.main import SQLTool

logger = get_logger(__name__)


class CustomerProductSQLInput(BaseModel):
    """Input schema for customer product SQL tool."""

    question: str = Field(description="Question about products or inventory")


class CustomerProductSQLTool(SQLTool):
    """SQL tool for customer product queries.

    Inherits from SQLTool. Restricts to Products/Inventory tables.
    """

    name: str = "product_query"
    description: str = (
        "Query product information from the database. "
        "Use this to get product details, prices, stock levels, and inventory."
    )
    args_schema: Type[BaseModel] = CustomerProductSQLInput
    allowed_tables: list[str] = []

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "tools_customer_product_sql",
        prompt_label: Optional[str] = None,
        allow_write: bool = False,
        allowed_tables: list[str] = None,
        **kwargs,
    ):
        """Initialize customer product SQL tool."""
        if allowed_tables is None:
            raise ValueError("allowed_tables is required")
        super().__init__(
            sql_client=sql_client,
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            prompt_name=prompt_name,
            prompt_label=prompt_label,
            allow_write=allow_write,
            **kwargs,
        )
        self.allowed_tables = allowed_tables
        logger.info("CustomerProductSQLTool initialized")

    def _get_schema_text(self) -> str:
        """Override: Get schema for allowed tables only."""
        schema_parts = []
        for table in self.allowed_tables:
            try:
                columns = self.sql_client.get_schema(table)
                col_defs = []
                for col in columns:
                    pk = " PK" if col.get("primary_key") else ""
                    nullable = "" if col.get("nullable") else " NOT NULL"
                    col_defs.append(f"{col['name']} {col['type']}{pk}{nullable}")
                schema_parts.append(f"{table}({', '.join(col_defs)})")
            except Exception as e:
                logger.warning(f"Could not get schema for {table}: {e}")
        return "\n".join(schema_parts)

    def _validate_tables(self, sql: str) -> bool:
        """Validate that SQL only accesses allowed tables."""
        sql_upper = sql.upper()
        all_tables = self.sql_client.get_tables()
        forbidden_tables = [t for t in all_tables if t not in self.allowed_tables]

        for table in forbidden_tables:
            if table.upper() in sql_upper:
                logger.warning(f"Forbidden table access attempted: {table}")
                return False
        return True

    def _run(self, question: str, context: Optional[dict] = None) -> dict:
        """Override: Execute with table validation."""
        logger.info(f"CustomerProductSQLTool processing: {question}")

        sql = self._generate_sql(question=question)
        logger.debug(f"Generated SQL: {sql}")

        if not self._validate_tables(sql):
            raise ValueError("Query rejected: Cannot access customer or order data.")

        if not self.validator.is_safe(sql):
            raise ValueError(f"SQL failed security validation: {sql}")

        results = self.sql_client.query(sql)
        logger.info(f"Query returned {len(results)} rows")
        return {"sql": sql, "results": results}
