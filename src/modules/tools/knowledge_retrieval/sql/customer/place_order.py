"""Customer place order tool - Create orders using LLM-generated SQL."""

import json
from typing import Optional, Type

from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from ..base.main import SQLTool

logger = get_logger(__name__)


class PlaceOrderInput(BaseModel):
    """Input schema for place order tool."""

    product_id: int = Field(description="Product ID to order")
    quantity: int = Field(description="Quantity to order", ge=1)
    confirmed: bool = Field(
        default=False,
        description="Set to true ONLY after user explicitly confirms the order. "
        "First call with confirmed=false to get order summary, "
        "then call again with confirmed=true after user says yes/ยืนยัน/confirm.",
    )


class PlaceOrderSQLTool(SQLTool):
    """Tool for placing customer orders.

    Inherits from SQLTool with allow_write=True.
    Uses LLM to generate SQL statements based on actual schema.
    """

    name: str = "place_order_sql"
    description: str = (
        "Place an order for a product. "
        "Use this when customer wants to buy/order a product. "
        "Requires product_id and quantity."
    )
    args_schema: Type[BaseModel] = PlaceOrderInput
    allowed_tables: list[str] = []
    customer_id: Optional[str] = None

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "tools_customer_place_order_sql",
        prompt_label: Optional[str] = None,
        allow_write: bool = True,
        allowed_tables: list[str] = None,
        customer_id: Optional[str] = None,
        **kwargs,
    ):
        """Initialize place order tool."""
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
        logger.info("PlaceOrderSQLTool initialized")

    def set_customer_id(self, customer_id: str) -> None:
        """Set customer ID for order."""
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

    def _generate_order_sql(self, product_id: int, quantity: int) -> dict:
        """Generate multiple SQL statements for order placement.

        Unlike base _generate_sql which returns a single SQL string,
        this returns a dict of SQL statements for multi-step order process:
        check_product, check_stock, insert_order, get_order_id, insert_details, update_inventory
        """
        prompt = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )

        variables = self._get_base_variables()
        variables.update(
            {
                "product_id": product_id,
                "quantity": quantity,
                "customer_id": self.customer_id,
            }
        )

        compiled = prompt.compile(**variables)

        response = self.llm_client.generate(prompt=compiled)

        try:
            # Strip markdown wrapper if present
            cleaned = response.strip()
            if cleaned.startswith("```"):
                # Remove ```json or ``` at start and ``` at end
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

    def _run(self, product_id: int, quantity: int, confirmed: bool = False) -> dict:
        """Execute order placement using LLM-generated SQL.

        If confirmed=False, returns order summary for user confirmation.
        If confirmed=True, actually places the order.
        """
        if not self.customer_id:
            return {"success": False, "error": "Customer ID not set"}

        logger.info(
            f"Place order request: product={product_id}, qty={quantity}, "
            f"customer={self.customer_id}, confirmed={confirmed}"
        )

        # Generate SQL statements
        try:
            sql_statements = self._generate_order_sql(product_id, quantity)
        except ValueError as e:
            return {"success": False, "error": str(e)}

        # Track executed stages
        executed_stages = {}

        # Step 1: Check product exists and get details
        check_product_sql = sql_statements.get("check_product")
        if not check_product_sql:
            return {"success": False, "error": "Failed to generate check_product SQL"}
        product_result = self.sql_client.query(check_product_sql)
        executed_stages["check_product"] = {
            "sql": check_product_sql,
            "result": product_result,
        }
        if not product_result:
            return {
                "success": False,
                "error": f"Product ID {product_id} not found",
                "stages": executed_stages,
            }

        # Get product info for confirmation
        product_info = product_result[0] if product_result else {}
        product_name = product_info.get("product_name", f"Product #{product_id}")
        price = product_info.get("price", 0)
        total_price = price * quantity

        # Step 2: Check stock
        check_stock_sql = sql_statements.get("check_stock")
        if not check_stock_sql:
            return {
                "success": False,
                "error": "Failed to generate check_stock SQL",
                "stages": executed_stages,
            }
        stock_result = self.sql_client.query(check_stock_sql)
        executed_stages["check_stock"] = {
            "sql": check_stock_sql,
            "result": stock_result,
        }
        available = self._get_first_value(stock_result) or 0
        if available < quantity:
            return {
                "success": False,
                "error": f"Insufficient stock. Requested: {quantity}, Available: {available}",
                "stages": executed_stages,
            }

        # If not confirmed, return summary for user confirmation (NO DB WRITE)
        if not confirmed:
            logger.info("Order not confirmed yet, returning summary for confirmation")
            return {
                "success": True,
                "needs_confirmation": True,
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity,
                "price_per_unit": price,
                "total_price": total_price,
                "available_stock": available,
                "message": f"Please confirm: Order {quantity}x {product_name} for ${total_price}?",
            }

        # Step 3: Insert order (only if confirmed=True)
        insert_order_sql = sql_statements.get("insert_order")
        if not insert_order_sql:
            return {
                "success": False,
                "error": "Failed to generate insert_order SQL",
                "stages": executed_stages,
            }
        self.sql_client.execute(insert_order_sql)
        executed_stages["insert_order"] = {"sql": insert_order_sql, "result": "OK"}

        # Step 4: Get order_id
        get_order_id_sql = sql_statements.get("get_order_id")
        if not get_order_id_sql:
            return {
                "success": False,
                "error": "Failed to generate get_order_id SQL",
                "stages": executed_stages,
            }
        order_result = self.sql_client.query(get_order_id_sql)
        executed_stages["get_order_id"] = {
            "sql": get_order_id_sql,
            "result": order_result,
        }
        order_id = self._get_first_value(order_result)
        if not order_id:
            return {
                "success": False,
                "error": "Failed to get order_id",
                "stages": executed_stages,
            }

        # Step 5: Insert order details
        insert_details_sql = sql_statements.get("insert_details")
        if not insert_details_sql:
            return {
                "success": False,
                "error": "Failed to generate insert_details SQL",
                "stages": executed_stages,
            }
        # Replace placeholder with actual order_id
        insert_details_sql = insert_details_sql.replace(
            "ORDER_ID_PLACEHOLDER", str(order_id)
        )
        self.sql_client.execute(insert_details_sql)
        executed_stages["insert_details"] = {
            "sql": insert_details_sql,
            "result": "OK",
        }

        # Step 6: Update inventory
        update_inventory_sql = sql_statements.get("update_inventory")
        if not update_inventory_sql:
            return {
                "success": False,
                "error": "Failed to generate update_inventory SQL",
                "stages": executed_stages,
            }
        self.sql_client.execute(update_inventory_sql)
        executed_stages["update_inventory"] = {
            "sql": update_inventory_sql,
            "result": "OK",
        }

        logger.info(f"Order placed successfully: order_id={order_id}")

        return {
            "success": True,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "stages": executed_stages,
        }
