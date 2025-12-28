"""PyPDF2 PDF parser implementation.

Simple text extraction using PyPDF2 library.
Fast and lightweight, but loses document structure.
"""

import os
from pathlib import Path
from typing import Any

from PyPDF2 import PdfReader

from libs.llm.parser.base import BasePDFParser
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class PDFParser(BasePDFParser):
    """PDF parser using PyPDF2 library.

    Provides simple text extraction without structure preservation.
    Best for quick extraction or when document structure is not important.
    """

    def __init__(self, **kwargs):
        """Initialize PyPDF2 parser.

        Args:
            **kwargs: Additional configuration (currently unused)
        """
        logger.info("Initialized PyPDF2 PDF parser")

    def parse(self, pdf_path: str, **kwargs) -> dict[str, Any]:
        """Parse PDF file and extract content with metadata.

        Args:
            pdf_path: Path to the PDF file
            **kwargs: Additional parser-specific parameters

        Returns:
            Dictionary containing:
                - text: Extracted text content (all pages combined)
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
            reader = PdfReader(str(pdf_path))

            # Extract text from all pages
            pages = self.parse_pages(pdf_path, **kwargs)
            full_text = "\n\n".join(page["text"] for page in pages)

            # Build metadata
            metadata = {
                "filename": pdf_path.name,
                "filepath": str(pdf_path.absolute()),
                "file_size": os.path.getsize(pdf_path),
                "num_pages": len(reader.pages),
            }

            # Add document info if available
            if reader.metadata:
                if reader.metadata.title:
                    metadata["title"] = reader.metadata.title
                if reader.metadata.author:
                    metadata["author"] = reader.metadata.author

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
            reader = PdfReader(str(pdf_path))
            pages = []

            for page_idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""

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

            logger.debug(f"Extracted {len(pages)} pages from {pdf_path.name}")
            return pages

        except Exception as e:
            logger.error(f"Error parsing pages from PDF {pdf_path}: {str(e)}")
            raise ValueError(f"Failed to parse PDF pages: {str(e)}") from e
