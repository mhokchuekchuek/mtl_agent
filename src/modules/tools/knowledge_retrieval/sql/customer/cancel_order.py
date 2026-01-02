"""Customer cancel order tool - Cancel orders using LLM-generated SQL."""

import json
from typing import Optional, Type

from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from ..base.main import SQLTool

logger = get_logger(__name__)


class CancelOrderInput(BaseModel):
    """Input schema for cancel order tool."""

    order_id: int = Field(description="Order ID to cancel")
    confirmed: bool = Field(
        default=False,
        description="Set to true ONLY after user explicitly confirms the cancellation. "
        "First call with confirmed=false to get order details, "
        "then call again with confirmed=true after user says yes/ยืนยัน/confirm.",
    )


class CancelOrderSQLTool(SQLTool):
    """Tool for cancelling customer orders.

    Inherits from SQLTool with allow_write=True.
    Uses LLM to generate SQL statements to:
    1. Verify order belongs to customer
    2. Check order is not already cancelled
    3. Update order status to 'cancelled'
    4. Restore inventory quantities
    """

    name: str = "cancel_order_sql"
    description: str = (
        "Cancel an order. "
        "Use this when customer wants to cancel their order. "
        "Requires order_id. Only orders belonging to the customer can be cancelled."
    )
    args_schema: Type[BaseModel] = CancelOrderInput
    allowed_tables: list[str] = []
    customer_id: Optional[str] = None

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "tools_customer_cancel_order_sql",
        prompt_label: Optional[str] = None,
        allow_write: bool = True,
        allowed_tables: list[str] = None,
        customer_id: Optional[str] = None,
        **kwargs,
    ):
        """Initialize cancel order tool."""
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
        logger.info("CancelOrderSQLTool initialized")

    def set_customer_id(self, customer_id: str) -> None:
        """Set customer ID for order cancellation."""
        self.customer_id = customer_id

    def _get_schema_text(self) -> str:
        """Get schema for allowed tables only."""
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

    def _generate_cancel_sql(self, order_id: int) -> dict:
        """Generate SQL statements for order cancellation.

        Returns a dict of SQL statements:
        check_order, check_status, get_order_details, update_status, restore_inventory
        """
        prompt = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )

        variables = self._get_base_variables()
        variables.update(
            {
                "order_id": order_id,
                "customer_id": self.customer_id,
            }
        )

        compiled = prompt.compile(**variables)

        response = self.llm_client.generate(prompt=compiled)

        try:
            # Strip markdown wrapper if present
            cleaned = response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                cleaned = "\n".join(lines)
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {response}")
            raise ValueError(f"Invalid LLM response format: {e}")

    def _get_first_value(self, result: list[dict]) -> any:
        """Extract first value from query result, regardless of column name."""
        if result and result[0]:
            return list(result[0].values())[0]
        return None

    def _run(self, order_id: int, confirmed: bool = False) -> dict:
        """Execute order cancellation using LLM-generated SQL.

        If confirmed=False, returns order details for user confirmation.
        If confirmed=True, actually cancels the order.
        """
        if not self.customer_id:
            return {"success": False, "error": "Customer ID not set"}

        logger.info(
            f"Cancel order request: order_id={order_id}, "
            f"customer={self.customer_id}, confirmed={confirmed}"
        )

        # Generate SQL statements
        try:
            sql_statements = self._generate_cancel_sql(order_id)
        except ValueError as e:
            return {"success": False, "error": str(e)}

        # Track executed stages
        executed_stages = {}

        # Step 1: Check order exists and belongs to customer
        check_order_sql = sql_statements.get("check_order")
        if not check_order_sql:
            return {"success": False, "error": "Failed to generate check_order SQL"}
        order_result = self.sql_client.query(check_order_sql)
        executed_stages["check_order"] = {
            "sql": check_order_sql,
            "result": order_result,
        }
        if not order_result:
            return {
                "success": False,
                "error": f"Order ID {order_id} not found or does not belong to you",
                "stages": executed_stages,
            }

        # Step 2: Check order status (not already cancelled)
        check_status_sql = sql_statements.get("check_status")
        if not check_status_sql:
            return {
                "success": False,
                "error": "Failed to generate check_status SQL",
                "stages": executed_stages,
            }
        status_result = self.sql_client.query(check_status_sql)
        executed_stages["check_status"] = {
            "sql": check_status_sql,
            "result": status_result,
        }
        current_status = self._get_first_value(status_result)
        if current_status == "cancelled":
            return {
                "success": False,
                "error": "Order is already cancelled",
                "stages": executed_stages,
            }

        # Step 3: Get order details for inventory restoration
        get_details_sql = sql_statements.get("get_order_details")
        if not get_details_sql:
            return {
                "success": False,
                "error": "Failed to generate get_order_details SQL",
                "stages": executed_stages,
            }
        details_result = self.sql_client.query(get_details_sql)
        executed_stages["get_order_details"] = {
            "sql": get_details_sql,
            "result": details_result,
        }

        # If not confirmed, return order details for user confirmation (NO DB WRITE)
        if not confirmed:
            logger.info(
                f"Cancel not confirmed yet, returning order details for confirmation"
            )
            # Get order summary from details
            order_info = order_result[0] if order_result else {}
            total_amount = order_info.get("total_amount", 0)
            order_date = order_info.get("order_date", "unknown")

            # Format product details
            products = []
            for detail in details_result:
                product_name = detail.get(
                    "product_name", f"Product #{detail.get('product_id', '?')}"
                )
                qty = detail.get("quantity", 0)
                products.append(f"{qty}x {product_name}")

            return {
                "success": True,
                "needs_confirmation": True,
                "order_id": order_id,
                "order_date": str(order_date),
                "total_amount": total_amount,
                "status": current_status,
                "products": products,
                "message": f"Please confirm: Cancel Order #{order_id} ({', '.join(products)}) for ${total_amount}?",
            }

        # Step 4: Update order status to cancelled (only if confirmed=True)
        update_status_sql = sql_statements.get("update_status")
        if not update_status_sql:
            return {
                "success": False,
                "error": "Failed to generate update_status SQL",
                "stages": executed_stages,
            }
        self.sql_client.execute(update_status_sql)
        executed_stages["update_status"] = {"sql": update_status_sql, "result": "OK"}

        # Step 5: Restore inventory for each order detail
        restore_inventory_sql = sql_statements.get("restore_inventory")
        if restore_inventory_sql:
            # May be a single SQL or need to execute per product
            # For simplicity, execute the generated SQL
            self.sql_client.execute(restore_inventory_sql)
            executed_stages["restore_inventory"] = {
                "sql": restore_inventory_sql,
                "result": "OK",
            }

        logger.info(f"Order cancelled successfully: order_id={order_id}")

        return {
            "success": True,
            "order_id": order_id,
            "previous_status": current_status,
            "new_status": "cancelled",
            "stages": executed_stages,
        }
