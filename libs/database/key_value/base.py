"""Base interface for key-value database clients."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseKeyValueClient(ABC):
    """Abstract base class for key-value database clients."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value by key."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set key-value pair with optional TTL in seconds."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete key."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass

    @abstractmethod
    def get_client(self) -> Any:
        """Get underlying client instance."""
        pass
