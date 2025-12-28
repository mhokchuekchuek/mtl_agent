"""Redis checkpointer repository implementation."""

from typing import Any, Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.redis import RedisSaver

from libs.database.key_value.base import BaseKeyValueClient
from src.repositories.checkpointers.base import BaseCheckpointerRepository


class RedisCheckpointerRepository(BaseCheckpointerRepository):
    """Redis-based checkpointer repository.

    Uses RedisSaver for LangGraph checkpoint persistence.
    """

    def __init__(
        self,
        redis_client: BaseKeyValueClient,
        ttl: int = 60,
        refresh_on_read: bool = True,
    ):
        """Initialize Redis checkpointer repository.

        Args:
            redis_client: Redis client instance.
            ttl: Time-to-live in minutes for checkpoints.
            refresh_on_read: Reset TTL when reading checkpoint.
        """
        ttl_config = {
            "default_ttl": ttl,
            "refresh_on_read": refresh_on_read,
        }

        self._checkpointer = RedisSaver(
            redis_client=redis_client.get_client(),
            ttl=ttl_config,
        )
        self._checkpointer.setup()

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
        # RedisSaver handles expiration via TTL
        pass
