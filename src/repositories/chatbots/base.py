"""Base interface for chatbot repositories."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import uuid4

from langchain_core.messages import BaseMessage

from src.repositories.checkpointers.base import BaseCheckpointerRepository
from src.repositories.stores.base import BaseStoreRepository


class BaseChatbotRepository(ABC):
    """Abstract base for chatbot repositories.

    Repositories compile workflows with memory (checkpointer + store).
    """

    def __init__(
        self,
        checkpoint_repo: Optional[BaseCheckpointerRepository] = None,
        store_repo: Optional[BaseStoreRepository] = None,
    ):
        self.checkpoint_repo = checkpoint_repo
        self.store_repo = store_repo

    @abstractmethod
    def invoke(
        self,
        query: str,
        thread_id: str,
        user_id: Optional[str] = None,
    ) -> dict:
        """Invoke the chatbot."""
        pass

    def get_history(self, thread_id: str) -> list[BaseMessage]:
        """Get conversation history for a thread."""
        if not self.checkpoint_repo:
            return []

        checkpoint = self.checkpoint_repo.get_checkpoint(thread_id)
        if checkpoint and checkpoint.checkpoint:
            return checkpoint.checkpoint.get("channel_values", {}).get("messages", [])
        return []

    def clear_conversation(self, thread_id: str) -> None:
        """Clear conversation memory for a thread."""
        if self.checkpoint_repo:
            self.checkpoint_repo.delete_checkpoint(thread_id)

    def _save_to_store(
        self,
        query: str,
        response: Optional[str],
        thread_id: str,
        user_id: Optional[str] = None,
    ) -> None:
        """Save conversation turn to long-term memory."""
        if not self.store_repo or not user_id:
            return

        namespace = ("users", user_id, "conversations")
        key = (
            f"{thread_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
        )

        self.store_repo.put(
            namespace=namespace,
            key=key,
            value={
                "query": query,
                "response": response,
                "thread_id": thread_id,
                "timestamp": datetime.now().isoformat(),
            },
        )
