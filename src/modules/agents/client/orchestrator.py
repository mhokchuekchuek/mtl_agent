"""Orchestrator agent for routing client chatbot requests."""

from datetime import datetime
from enum import Enum
from typing import Any
from zoneinfo import ZoneInfo

from langchain_openai import ChatOpenAI

from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger
from src.modules.agents.base import BaseAgent

logger = get_logger(__name__)


class Intent(str, Enum):
    """Possible intents for client chatbot."""

    CHAT_HISTORY = "chat_history"
    INSIGHT = "insight"


class OrchestratorAgent(BaseAgent):
    """Router agent that classifies intent and routes to appropriate agent.

    Decides whether the user query is:
    - chat_history: Looking up customer conversations
    - insight: BI analytics / reporting / visualization
    """

    def __init__(
        self,
        llm: ChatOpenAI,
        prompt_manager: BasePromptManager,
        prompt_name: str = "client_chatbot_orchestrator",
        prompt_label: str | None = None,
    ):
        """Initialize orchestrator agent.

        Args:
            llm: ChatOpenAI instance.
            prompt_manager: Prompt manager for retrieving prompts.
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Label for prompt retrieval.
        """
        super().__init__(name="orchestrator")
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Classify intent from query.

        Args:
            state: Current state with keys:
                - translated_query: str - query in English

        Returns:
            Updated state with:
                - intent: Intent - classified intent
        """
        query = state.get("translated_query", state.get("query", ""))

        if not query:
            logger.warning("No query provided, defaulting to insight")
            return {"intent": Intent.INSIGHT}

        try:
            prompt_obj = self.prompt_manager.get_prompt(
                self.prompt_name,
                label=self.prompt_label,
            )

            # Compile prompt with current datetime context
            tz = ZoneInfo("Asia/Bangkok")
            now = datetime.now(tz)
            system_prompt = prompt_obj.compile(
                current_datetime=now.strftime("%Y-%m-%d %H:%M"),
                timezone="Asia/Bangkok",
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ]

            response = self.llm.invoke(messages)
            intent_str = response.content.strip().lower()

            # Parse response to Intent
            if "chat_history" in intent_str or "chat" in intent_str:
                intent = Intent.CHAT_HISTORY
            else:
                intent = Intent.INSIGHT

            logger.info(f"Classified intent: {intent.value} for query: {query[:50]}...")
            return {"intent": intent}

        except Exception as e:
            logger.error(f"Orchestrator classification failed: {e}")
            # Default to insight on error
            return {"intent": Intent.INSIGHT}
