"""Key-value database selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class KeyValueSelector(BaseToolSelector):
    """Selector for key-value database providers.

    Available providers:
        - redis: Redis client

    Example:
        >>> from libs.database.key_value.selector import KeyValueSelector
        >>> client = KeyValueSelector.create(
        ...     provider="redis",
        ...     host="localhost",
        ...     port=6379,
        ... )
        >>> client.set("key", "value")
        >>> client.get("key")
        >>> # For LangGraph checkpointer
        >>> redis_client = client.get_client()
    """

    _PROVIDERS = {
        "redis": "libs.database.key_value.redis.main.RedisClient",
    }
