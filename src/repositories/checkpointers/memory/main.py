"""Memory checkpointer repository implementation."""

from typing import Any, Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver

from src.repositories.checkpointers.base import BaseCheckpointerRepository


class MemoryCheckpointerRepository(BaseCheckpointerRepository):
    """In-memory checkpointer repository.

    Uses MemorySaver for development/testing.
    Data is lost when process ends.
    """

    def __init__(self):
        """Initialize Memory checkpointer repository."""
        self._checkpointer = MemorySaver()

    @property
    def checkpointer(self) -> BaseCheckpointSaver:
        """Get underlying checkpointer for workflow injection."""
        return self._checkpointer

    def get_checkpoint(self, thread_id: str) -> Optional[Any]:
        """Get checkpoint for a thread."""
        config = {"configurable": {"thread_id": thread_id}}
        return self._checkpointer.get_tuple(config)

    def delete_checkpoint(self, thread_id: str) -> None:
        """Delete checkpoint for a thread."""
        # MemorySaver doesn't support delete
        pass
