"""Client analytics SQL tool - All tables, read-only."""

from typing import Optional, Type

from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from ..base.main import SQLTool

logger = get_logger(__name__)


class ClientAnalyticsSQLInput(BaseModel):
    """Input schema for client analytics SQL tool."""

    question: str = Field(description="Analytics question about business data")


class ClientAnalyticsSQLTool(SQLTool):
    """SQL tool for client BI analytics.

    Inherits from SQLTool. Access to all tables, read-only.
    """

    name: str = "analytics_query"
    description: str = (
        "Query business data for analytics. "
        "Use this for revenue, orders, customers, products, and inventory analysis."
    )
    args_schema: Type[BaseModel] = ClientAnalyticsSQLInput

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "tools_client_analytics_sql",
        prompt_label: Optional[str] = None,
        **kwargs,
    ):
        """Initialize client analytics SQL tool."""
        super().__init__(
            sql_client=sql_client,
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            prompt_name=prompt_name,
            prompt_label=prompt_label,
            allow_write=False,
            **kwargs,
        )
        logger.info("ClientAnalyticsSQLTool initialized")
