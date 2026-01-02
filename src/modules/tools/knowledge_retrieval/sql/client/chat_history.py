"""Client chat history SQL tool - PostgreSQL store."""

from typing import Optional, Type

from pydantic import BaseModel, Field

from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

from ..base.main import SQLTool

logger = get_logger(__name__)


class ClientChatHistorySQLInput(BaseModel):
    """Input schema for client chat history SQL tool."""

    question: str = Field(description="Question about chat conversation history")


class ClientChatHistorySQLTool(SQLTool):
    """SQL tool for querying chat history from PostgreSQL store.

    Inherits from SQLTool. Queries the LangGraph store table.
    """

    name: str = "chat_history_query"
    description: str = (
        "Query customer chat conversation history. "
        "Use this to find what customers asked or said in previous conversations."
    )
    args_schema: Type[BaseModel] = ClientChatHistorySQLInput

    def __init__(
        self,
        sql_client: BaseSQLDatabase,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "tools_client_chat_history_sql",
        prompt_label: Optional[str] = None,
        **kwargs,
    ):
        """Initialize client chat history SQL tool."""
        super().__init__(
            sql_client=sql_client,
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            prompt_name=prompt_name,
            prompt_label=prompt_label,
            allow_write=False,
            **kwargs,
        )
        logger.info("ClientChatHistorySQLTool initialized")
