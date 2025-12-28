"""Base interface for store repositories."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from langgraph.store.base import BaseStore


class BaseStoreRepository(ABC):
    """Abstract base for store repositories.

    Stores provide long-term memory that persists across conversations.
    Unlike checkpointers (short-term, per-thread), stores enable:
    - Cross-thread memory sharing
    - Conversation summaries
    - User preferences
    - Semantic search over past interactions
    """

    @property
    @abstractmethod
    def store(self) -> BaseStore:
        """Get underlying store for workflow injection."""
        pass

    @abstractmethod
    def put(
        self,
        namespace: tuple[str, ...],
        key: str,
        value: dict[str, Any],
    ) -> None:
        """Store a value."""
        pass

    @abstractmethod
    def get(
        self,
        namespace: tuple[str, ...],
        key: str,
    ) -> Optional[dict[str, Any]]:
        """Retrieve a value."""
        pass

    @abstractmethod
    def search(
        self,
        namespace: tuple[str, ...],
        query: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search for values in namespace."""
        pass

    @abstractmethod
    def delete(
        self,
        namespace: tuple[str, ...],
        key: str,
    ) -> None:
        """Delete a value."""
        pass
