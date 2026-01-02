from abc import ABC, abstractmethod
from typing import Any

from libs.logger.logger import get_logger


class BaseAgent(ABC):
    """Abstract base class for all agents.

    All agents should inherit from this class and implement
    the execute method to process the agent state.

    Attributes:
        name: Unique identifier for this agent.
        logger: Logger instance for this agent.
    """

    def __init__(self, name: str):
        """Initialize the agent.

        Args:
            name: Unique identifier for this agent.
        """
        self.name = name
        self.logger = get_logger(f"agent.{name}")

    @abstractmethod
    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's logic on the current state.

        Args:
            state: Current agent state with messages, context, etc.

        Returns:
            Updated agent state after processing.
        """
        pass

    def _build_messages_with_history(
        self, query: str, history: list
    ) -> list[dict[str, str]]:
        """Build messages list including conversation history.

        Converts LangChain message objects (AIMessage, HumanMessage, ToolMessage)
        into a list of role/content dicts for agent consumption.

        Args:
            query: Current user query.
            history: List of previous messages from state.

        Returns:
            List of message dicts with role and content.
        """
        messages = []

        for msg in history:
            msg_type = getattr(msg, "type", None)
            content = getattr(msg, "content", str(msg))

            if msg_type == "ai" or msg_type == "assistant":
                messages.append({"role": "assistant", "content": content})
            elif msg_type == "human" or msg_type == "user":
                messages.append({"role": "user", "content": content})
            elif msg_type == "tool":
                tool_name = getattr(msg, "name", "tool")
                messages.append(
                    {
                        "role": "assistant",
                        "content": f"[Tool Result from {tool_name}]: {content}",
                    }
                )

        messages.append({"role": "user", "content": query})

        return messages
