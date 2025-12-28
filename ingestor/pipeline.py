"""PDF ingestion pipeline.

Orchestrates: Parse PDF → Extract structured data → Embed → Store in Qdrant.
"""

import re
from pathlib import Path
from typing import Any

from ingestor.extractor.base import BaseExtractor
from libs.database.vector.base import BaseVectorStore
from libs.llm.client.base import BaseLLM
from libs.llm.parser.base import BasePDFParser
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class IngestionPipeline:
    """Pipeline for ingesting product PDFs into vector store.

    Flow:
        1. Parse PDF → raw text/markdown
        2. Extract structured data via LLM
        3. Generate embeddings from extracted content
        4. Store in Qdrant with metadata
    """

    def __init__(
        self,
        parser: BasePDFParser,
        extractor: BaseExtractor,
        llm_client: BaseLLM,
        vector_store: BaseVectorStore,
        batch_size: int = 10,
    ):
        """Initialize pipeline.

        Args:
            parser: PDF parser instance (pypdf2 or docling).
            extractor: LLM extractor for structured data extraction.
            llm_client: LLM client with embed() method.
            vector_store: Vector store for embedding storage.
            batch_size: Batch size for embedding generation.
        """
        self.parser = parser
        self.extractor = extractor
        self.llm = llm_client
        self.vector_store = vector_store
        self.batch_size = batch_size

    def ingest(self, source_dir: Path | str) -> dict[str, Any]:
        """Ingest all PDFs from source directory.

        Args:
            source_dir: Directory containing PDF files.

        Returns:
            Summary dict with counts and any errors.
        """
        source_dir = Path(source_dir)
        pdf_files = list(source_dir.glob("*.pdf"))

        logger.info(f"Found {len(pdf_files)} PDF files in {source_dir}")

        results = {
            "total": len(pdf_files),
            "success": 0,
            "failed": 0,
            "errors": [],
        }

        # Process in batches
        batch = []
        for pdf_path in pdf_files:
            try:
                product_data = self._process_pdf(pdf_path)
                batch.append(product_data)

                if len(batch) >= self.batch_size:
                    self._store_batch(batch)
                    results["success"] += len(batch)
                    batch = []

            except Exception as e:
                logger.error(f"Failed to process {pdf_path.name}: {e}")
                results["failed"] += 1
                results["errors"].append({"file": pdf_path.name, "error": str(e)})

        # Store remaining batch
        if batch:
            self._store_batch(batch)
            results["success"] += len(batch)

        logger.info(
            f"Ingestion complete: {results['success']}/{results['total']} successful"
        )
        return results

    def ingest_single(self, pdf_path: Path | str) -> dict[str, Any]:
        """Ingest a single PDF file.

        Args:
            pdf_path: Path to PDF file.

        Returns:
            Extracted product data with embedding stored.
        """
        pdf_path = Path(pdf_path)
        product_data = self._process_pdf(pdf_path)
        self._store_batch([product_data])
        return product_data

    def _process_pdf(self, pdf_path: Path) -> dict[str, Any]:
        """Process single PDF: parse and extract.

        Args:
            pdf_path: Path to PDF file.

        Returns:
            Extracted product data with metadata.
        """
        # Extract product_id from filename (e.g., "1_espresso_coffee_maker.pdf" → 1)
        product_id = self._extract_product_id(pdf_path.name)

        # Parse PDF to text
        logger.debug(f"Parsing {pdf_path.name}")
        parsed = self.parser.parse(str(pdf_path))
        text = parsed["text"]

        # Extract structured data via LLM
        logger.debug(f"Extracting data from {pdf_path.name}")
        extracted = self.extractor.extract(text, product_id=product_id)

        # Add metadata
        extracted["product_id"] = product_id
        extracted["source_file"] = pdf_path.name
        extracted["page_count"] = parsed.get("pages", 1)

        return extracted

    def _extract_product_id(self, filename: str) -> int:
        """Extract product ID from filename.

        Args:
            filename: PDF filename (e.g., "1_espresso_coffee_maker.pdf").

        Returns:
            Product ID as integer.

        Raises:
            ValueError: If product ID cannot be extracted.
        """
        match = re.match(r"^(\d+)_", filename)
        if match:
            return int(match.group(1))
        raise ValueError(f"Cannot extract product_id from filename: {filename}")

    def _store_batch(self, batch: list[dict[str, Any]]) -> None:
        """Generate embeddings and store batch in vector store.

        Args:
            batch: List of extracted product data dicts.
        """
        if not batch:
            return

        # Create text for embedding (combine key fields)
        texts = []
        for product in batch:
            text_parts = [
                product.get("product_name", ""),
                product.get("description", ""),
            ]

            # Add specs as text
            specs = product.get("specifications", {})
            if specs:
                spec_text = ", ".join(f"{k}: {v}" for k, v in specs.items())
                text_parts.append(spec_text)

            # Add features as text
            features = product.get("features", [])
            if features:
                feature_text = ". ".join(
                    f"{f.get('title', '')}: {f.get('description', '')}"
                    for f in features
                )
                text_parts.append(feature_text)

            texts.append(" ".join(filter(None, text_parts)))

        # Generate embeddings
        logger.debug(f"Generating embeddings for {len(texts)} products")
        embeddings = self.llm.embed(texts)

        # Prepare metadata for vector store
        metadata = []
        for product, text in zip(batch, texts):
            meta = {
                "product_id": product.get("product_id"),
                "product_name": product.get("product_name", ""),
                "source_file": product.get("source_file", ""),
                "text": text,  # Store full text for retrieval
            }
            metadata.append(meta)

        # Store in vector store
        ids = [int(product.get("product_id")) for product in batch]
        self.vector_store.add(embeddings=embeddings, metadata=metadata, ids=ids)

        logger.info(f"Stored {len(batch)} products in vector store")
