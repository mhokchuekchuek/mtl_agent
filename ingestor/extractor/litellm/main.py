"""LiteLLM-based product data extractor.

Uses LLM to extract structured product information from PDF text content.
"""

import json
import re
from typing import Any

from ingestor.extractor.base import BaseExtractor
from libs.llm.client.base import BaseLLM
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class LLMExtractor(BaseExtractor):
    """Extract structured product data using LLM."""

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt: Any,
        **kwargs,
    ):
        """Initialize extractor.

        Args:
            llm_client: LLM client instance for text generation.
            prompt: Langfuse prompt object with compile() method.
            **kwargs: Additional arguments.
        """
        self.llm = llm_client
        self.prompt = prompt

    def extract(self, text: str, **kwargs) -> dict[str, Any]:
        """Extract structured product data from text.

        Args:
            text: Raw text content from PDF.
            **kwargs: Additional options (e.g., product_id from filename).

        Returns:
            Structured product data with fields:
                - product_name: str
                - description: str
                - specifications: dict
                - features: list[dict]
                - summary: str
        """
        prompt = self._build_prompt(text)

        response = self.llm.generate(prompt)

        extracted = self._parse_response(response)

        if "product_id" in kwargs:
            extracted["product_id"] = kwargs["product_id"]

        return extracted

    def _build_prompt(self, text: str) -> str:
        """Build extraction prompt.

        Args:
            text: Raw text content to include in prompt.

        Returns:
            Compiled prompt string.
        """
        return self.prompt.compile(text=text)

    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse LLM response to extract JSON.

        Args:
            response: Raw LLM response string.

        Returns:
            Parsed dictionary with product data.
        """
        json_match = re.search(r"\{[\s\S]*\}", response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            "product_name": "",
            "description": "",
            "specifications": {},
            "features": [],
            "summary": "",
            "_raw_response": response,
            "_parse_error": True,
        }
