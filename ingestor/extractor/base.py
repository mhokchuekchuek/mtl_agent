"""Base abstraction for data extractors."""

from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    """Abstract base class for data extractors.

    Extractors take raw text and extract structured data
    based on a predefined schema.
    """

    @abstractmethod
    def extract(self, text: str, **kwargs) -> dict[str, Any]:
        """Extract structured data from text.

        Args:
            text: Raw text content to extract from
            **kwargs: Additional extractor-specific parameters

        Returns:
            Dictionary containing extracted structured data

        Raises:
            ValueError: If text is empty or extraction fails
        """
        pass
