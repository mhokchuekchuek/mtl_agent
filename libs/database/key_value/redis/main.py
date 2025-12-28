"""Redis client implementation."""

from typing import Any, Optional

from redis import Redis

from libs.database.key_value.base import BaseKeyValueClient
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class RedisClient(BaseKeyValueClient):
    """Redis client wrapper.

    Provides a simple interface for Redis operations and exposes
    the underlying client for use with LangGraph checkpointers.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        ssl: bool = False,
        decode_responses: bool = False,
    ):
        """Initialize Redis client.

        Args:
            host: Redis server host.
            port: Redis server port.
            db: Redis database number.
            password: Redis password (optional).
            ssl: Enable SSL connection.
            decode_responses: Decode responses to strings.
        """
        self._client = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            ssl=ssl,
            decode_responses=decode_responses,
        )
        logger.info(f"Redis client initialized (host={host}, port={port}, db={db})")

    def get(self, key: str) -> Optional[Any]:
        """Get value by key."""
        return self._client.get(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set key-value pair with optional TTL in seconds."""
        if ttl:
            self._client.setex(key, ttl, value)
        else:
            self._client.set(key, value)

    def delete(self, key: str) -> None:
        """Delete key."""
        self._client.delete(key)

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return bool(self._client.exists(key))

    def get_client(self) -> Redis:
        """Get underlying Redis client instance.

        Use this to pass to LangGraph RedisSaver:
            redis_client = RedisClient(host="localhost", port=6379)
            checkpointer = RedisSaver(redis_client=redis_client.get_client())
        """
        return self._client
