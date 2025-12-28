"""Docling PDF parser implementation.

PDF parsing with layout analysis and markdown export.
Preserves document structure for better RAG quality.

Reference: https://github.com/DS4SD/docling
"""

import os
from pathlib import Path
from typing import Any

from docling.document_converter import DocumentConverter

from libs.llm.parser.base import BasePDFParser
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class PDFParser(BasePDFParser):
    """PDF parser using Docling library.

    Provides modern PDF parsing with layout analysis,
    table extraction, and markdown output.
    """

    def __init__(self, **kwargs):
        """Initialize Docling PDF parser.

        Args:
            **kwargs: Additional configuration for DocumentConverter
        """
        self.converter = DocumentConverter(**kwargs)
        logger.info("Initialized Docling PDF parser")

    def parse(self, pdf_path: str, **kwargs) -> dict[str, Any]:
        """Parse PDF file and extract content with metadata.

        Args:
            pdf_path: Path to the PDF file
            **kwargs: Additional parser-specific parameters

        Returns:
            Dictionary containing:
                - text: Extracted text content (markdown format)
                - metadata: Dictionary with file metadata
                - pages: List of page-wise content

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF is invalid or corrupted
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.suffix.lower() == ".pdf":
            raise ValueError(f"File is not a PDF: {pdf_path}")

        logger.info(f"Parsing PDF: {pdf_path}")

        try:
            # Convert PDF using Docling
            result = self.converter.convert(str(pdf_path))

            # Extract full text as markdown
            full_text = result.document.export_to_markdown()

            # Extract metadata
            metadata = {
                "filename": pdf_path.name,
                "filepath": str(pdf_path.absolute()),
                "file_size": os.path.getsize(pdf_path),
            }

            # Add document metadata if available
            if hasattr(result.document, "metadata"):
                doc_metadata = result.document.metadata
                if hasattr(doc_metadata, "title") and doc_metadata.title:
                    metadata["title"] = doc_metadata.title
                if hasattr(doc_metadata, "author") and doc_metadata.author:
                    metadata["author"] = doc_metadata.author

            # Extract pages
            pages = self.parse_pages(pdf_path, _result=result, **kwargs)
            metadata["num_pages"] = len(pages)

            logger.info(
                f"Successfully parsed PDF: {pdf_path.name} ({len(pages)} pages)"
            )

            return {
                "text": full_text,
                "metadata": metadata,
                "pages": pages,
            }

        except Exception as e:
            logger.error(f"Error parsing PDF {pdf_path}: {str(e)}")
            raise ValueError(f"Failed to parse PDF: {str(e)}") from e

    def parse_pages(self, pdf_path: str, **kwargs) -> list[dict[str, Any]]:
        """Parse PDF and return content organized by pages.

        Args:
            pdf_path: Path to the PDF file
            **kwargs: Additional parser-specific parameters
                _result: Pre-computed Docling result (optional)

        Returns:
            List of dictionaries, one per page

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF is invalid or corrupted
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        logger.debug(f"Parsing pages from PDF: {pdf_path}")

        try:
            # Use pre-computed result if available
            result = kwargs.get("_result")
            if result is None:
                result = self.converter.convert(str(pdf_path))

            pages = []

            # Extract page-wise content
            if hasattr(result.document, "pages"):
                for page_idx, page in enumerate(result.document.pages):
                    page_text = (
                        page.export_to_markdown()
                        if hasattr(page, "export_to_markdown")
                        else str(page)
                    )

                    pages.append(
                        {
                            "page_number": page_idx,
                            "text": page_text,
                            "metadata": {
                                "page_number": page_idx,
                                "filename": pdf_path.name,
                            },
                        }
                    )
            else:
                # Fallback: treat entire document as single page
                full_text = result.document.export_to_markdown()
                pages.append(
                    {
                        "page_number": 0,
                        "text": full_text,
                        "metadata": {
                            "page_number": 0,
                            "filename": pdf_path.name,
                        },
                    }
                )

            logger.debug(f"Extracted {len(pages)} pages from {pdf_path.name}")
            return pages

        except Exception as e:
            logger.error(f"Error parsing pages from PDF {pdf_path}: {str(e)}")
            raise ValueError(f"Failed to parse PDF pages: {str(e)}") from e
