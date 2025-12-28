"""Extractor selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class ExtractorSelector(BaseToolSelector):
    """Selector for data extractor providers.

    Available providers:
        - litellm: LLM-based structured data extraction

    Example:
        >>> from ingestor.extractor.selector import ExtractorSelector
        >>> extractor = ExtractorSelector.create(provider="litellm", llm_client=client)
        >>> result = extractor.extract(text)
    """

    _PROVIDERS = {
        "litellm": "ingestor.extractor.litellm.main.LLMExtractor",
    }
