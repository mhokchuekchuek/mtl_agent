"""State definitions for customer chatbot workflow."""

from typing import Annotated, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


def add_steps(existing: list[dict], new: list[dict]) -> list[dict]:
    """Reducer to accumulate steps."""
    return existing + new


class ShoppingState(TypedDict):
    """State passed between nodes in the customer chatbot workflow.

    Attributes:
        messages: Message history with automatic accumulation.
        query: User's raw query.
        customer_id: Customer ID for order placement.
        user_language: Detected user language ("th" or "en").
        translated_query: Query translated to English (if needed).
        response: Final response in user's language.
        error: Error message if any step failed.
        steps: List of I/O for each agent/tool executed.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    query: str
    customer_id: Optional[str]
    user_language: Optional[str]
    translated_query: Optional[str]
    response: Optional[str]
    error: Optional[str]
    steps: Annotated[list[dict], add_steps]


def create_initial_state(query: str, customer_id: str | None = None) -> ShoppingState:
    """Create initial state from a user query.

    Args:
        query: User query to process.
        customer_id: Optional customer ID for order placement.

    Returns:
        Initial ShoppingState with the query set.
    """
    return ShoppingState(
        messages=[],
        query=query,
        customer_id=customer_id,
        user_language=None,
        translated_query=None,
        response=None,
        error=None,
        steps=[],
    )
