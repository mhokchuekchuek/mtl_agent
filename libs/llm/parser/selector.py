"""Parser selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class ParserSelector(BaseToolSelector):
    """Selector for PDF parser providers.

    Available providers:
        - pypdf2: Simple text extraction (fast, lightweight)
        - docling: Markdown output with structure preservation

    Example:
        >>> from libs.llm.parser.selector import ParserSelector
        >>> parser = ParserSelector.create(provider="pypdf2")
        >>> result = parser.parse("document.pdf")
    """

    _PROVIDERS = {
        "pypdf2": "libs.llm.parser.pypdf2.main.PDFParser",
        "docling": "libs.llm.parser.docling.main.PDFParser",
    }
