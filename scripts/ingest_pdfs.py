#!/usr/bin/env python3
"""PDF Ingestion Script (Config-driven).

Reads settings from configs/ingestor/settings.yaml

Usage:
    python scripts/ingest_pdfs.py

Override via environment:
    INGESTOR__PARSER=pypdf2 python scripts/ingest_pdfs.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ingestor.extractor.selector import ExtractorSelector
from ingestor.pipeline import IngestionPipeline
from libs.configs.selector import ConfigSelector
from libs.database.vector.selector import VectorStoreSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.parser.selector import ParserSelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from libs.logger.logger import get_logger, setup_logging

settings = ConfigSelector.create(provider="dynaconf")
setup_logging(level=settings.get("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)


def main() -> int:
    """Main entry point."""
    # 1. Get config values
    parser_provider = settings.get("ingestor.parser", "docling")
    pdf_dir = Path(settings.get("ingestor.pdf_dir", "data/product_details"))
    batch_size = settings.get("ingestor.batch_size", 10)

    # Validate
    if not pdf_dir.exists():
        logger.error(f"PDF directory not found: {pdf_dir}")
        return 1

    pdf_count = len(list(pdf_dir.glob("*.pdf")))
    if pdf_count == 0:
        logger.error(f"No PDF files found in {pdf_dir}")
        return 1

    logger.info(f"Starting ingestion of {pdf_count} PDFs from {pdf_dir}")
    logger.info(f"Parser: {parser_provider}")

    # 2. Create components via selectors
    parser = ParserSelector.create(provider=parser_provider)

    llm_client = LLMClientSelector.create(
        provider="litellm",
        proxy_url=settings.get("ingestor.llm.proxy_url"),
        api_key=settings.get("ingestor.llm.api_key"),
        completion_model=settings.get("ingestor.llm.completion_model"),
        embedding_model=settings.get("ingestor.llm.embedding_model"),
    )

    prompt_manager = PromptManagerSelector.create(
        provider=settings.get("prompt_manager.langfuse.provider", "langfuse"),
        public_key=settings.get("prompt_manager.langfuse.public_key"),
        secret_key=settings.get("prompt_manager.langfuse.secret_key"),
        host=settings.get("prompt_manager.langfuse.host"),
    )

    # Fetch prompt with label from config
    prompt_name = settings.get(
        "ingestor.prompts.extractor.name", "ingestor_extract_product"
    )
    prompt_label = settings.get("ingestor.prompts.extractor.label")
    prompt = prompt_manager.get_prompt(prompt_name, label=prompt_label)

    extractor = ExtractorSelector.create(
        provider="litellm",
        llm_client=llm_client,
        prompt=prompt,
    )

    vector_store = VectorStoreSelector.create(
        provider="qdrant",
        host=settings.get("ingestor.qdrant.host"),
        port=settings.get("ingestor.qdrant.port"),
        collection_name=settings.get("ingestor.qdrant.collection"),
        vector_size=settings.get("ingestor.qdrant.vector_size"),
    )

    # 3. Create pipeline and run
    pipeline = IngestionPipeline(
        parser=parser,
        extractor=extractor,
        llm_client=llm_client,
        vector_store=vector_store,
        batch_size=batch_size,
    )

    results = pipeline.ingest(pdf_dir)

    # 4. Print summary
    print("\n" + "=" * 50)
    print("Ingestion Summary")
    print("=" * 50)
    print(f"Total PDFs:     {results['total']}")
    print(f"Successful:     {results['success']}")
    print(f"Failed:         {results['failed']}")

    if results["errors"]:
        print("\nErrors:")
        for error in results["errors"]:
            print(f"  - {error['file']}: {error['error']}")

    print("=" * 50)

    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
