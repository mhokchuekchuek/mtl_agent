"""Generic chatbot use case - application business logic."""

from typing import Optional

from langchain_core.messages import BaseMessage

from src.repositories.chatbots.base import BaseChatbotRepository


class ChatbotService:
    """Chatbot service for user interactions.

    Works with any chatbot repository implementation.
    """

    def __init__(self, chatbot_repo: BaseChatbotRepository):
        self._repo = chatbot_repo

    def chat(
        self,
        query: str,
        thread_id: str,
        user_id: Optional[str] = None,
    ) -> dict:
        """Process a chat query.

        Args:
            query: User's message.
            thread_id: Conversation thread identifier.
            user_id: Optional user ID for observability.

        Returns:
            Response state dictionary.
        """
        return self._repo.invoke(query, thread_id, user_id)

    def get_history(self, thread_id: str) -> list[BaseMessage]:
        """Get conversation history."""
        return self._repo.get_history(thread_id)

    def clear_conversation(self, thread_id: str) -> None:
        """Clear conversation memory."""
        self._repo.clear_conversation(thread_id)
