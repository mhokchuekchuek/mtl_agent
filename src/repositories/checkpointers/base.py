"""Base interface for checkpointer repositories."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from langgraph.checkpoint.base import BaseCheckpointSaver


class BaseCheckpointerRepository(ABC):
    """Abstract base for checkpointer repositories."""

    @property
    @abstractmethod
    def checkpointer(self) -> BaseCheckpointSaver:
        """Get underlying checkpointer for workflow injection."""
        pass

    @abstractmethod
    def get_checkpoint(self, thread_id: str) -> Optional[Any]:
        """Get checkpoint for a thread."""
        pass

    @abstractmethod
    def delete_checkpoint(self, thread_id: str) -> None:
        """Delete checkpoint for a thread."""
        pass
