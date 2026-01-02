"""Customer order SQL tool - Orders with customer_id filter via prompt."""

from typing import Optional, Type

from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from ..base.main import SQLTool

logger = get_logger(__name__)


class CustomerOrderSQLInput(BaseModel):
    """Input schema for customer order SQL tool."""

    question: str = Field(description="Question about your orders")


class CustomerOrderSQLTool(SQLTool):
    """SQL tool for customer order queries.

    Inherits from SQLTool. Restricts to Orders/OrderDetails tables.
    Uses prompt with customer_id to generate filtered queries.
    """

    name: str = "order_query"
    description: str = (
        "Query your order history from the database. "
        "Use this to check your orders, order status, and purchase history."
    )
    args_schema: Type[BaseModel] = CustomerOrderSQLInput
    allowed_tables: list[str] = []
    customer_id: Optional[str] = None

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "tools_customer_order_sql",
        prompt_label: Optional[str] = None,
        allow_write: bool = False,
        allowed_tables: list[str] = None,
        customer_id: Optional[str] = None,
        **kwargs,
    ):
        """Initialize customer order SQL tool."""
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
        self.customer_id = customer_id
        logger.info("CustomerOrderSQLTool initialized")

    def set_customer_id(self, customer_id: str) -> None:
        """Set customer ID for query filtering."""
        self.customer_id = customer_id

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

    def _validate_customer_filter(self, sql: str) -> bool:
        """Validate that SQL contains customer_id filter."""
        if not self.customer_id:
            return False
        return self.customer_id in sql

    def _run(self, question: str, context: Optional[dict] = None) -> dict:
        """Override: Execute with table and customer_id validation."""
        if not self.customer_id:
            raise ValueError("Customer ID not set. Cannot query orders.")

        logger.info(f"CustomerOrderSQLTool processing: {question}")

        sql = self._generate_sql(
            question=question,
            customer_id=self.customer_id,
        )
        logger.debug(f"Generated SQL: {sql}")

        if not self._validate_tables(sql):
            raise ValueError("Query rejected: Cannot access forbidden tables.")

        if not self._validate_customer_filter(sql):
            raise ValueError("Query rejected: Missing customer_id filter.")

        if not self.validator.is_safe(sql):
            raise ValueError(f"SQL failed security validation: {sql}")

        results = self.sql_client.query(sql)
        logger.info(f"Query returned {len(results)} rows")
        return {"sql": sql, "results": results}
