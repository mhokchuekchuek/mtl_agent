"""State definitions for client chatbot workflow."""

from typing import Annotated, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from src.modules.agents.client.orchestrator import Intent


def add_steps(existing: list[dict], new: list[dict]) -> list[dict]:
    """Reducer to accumulate steps."""
    return existing + new


class ClientChatbotState(TypedDict):
    """State passed between nodes in the client chatbot workflow.

    Attributes:
        messages: Message history with automatic accumulation.
        query: User's raw query.
        user_language: Detected user language ("th" or "en").
        translated_query: Query translated to English (if needed).
        intent: Classified intent (chat_history or insight).
        response: Final response in user's language.
        chart_html: Plotly chart HTML if visualization was created.
        error: Error message if any step failed.
        steps: List of I/O for each agent/tool executed.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    query: str
    user_language: Optional[str]
    translated_query: Optional[str]
    intent: Optional[Intent]
    response: Optional[str]
    chart_html: Optional[str]
    error: Optional[str]
    steps: Annotated[list[dict], add_steps]


def create_initial_state(query: str) -> ClientChatbotState:
    """Create initial state from a user query.

    Args:
        query: User query to process.

    Returns:
        Initial ClientChatbotState with the query set.
    """
    return ClientChatbotState(
        messages=[],
        query=query,
        user_language=None,
        translated_query=None,
        intent=None,
        response=None,
        chart_html=None,
        error=None,
        steps=[],
    )
