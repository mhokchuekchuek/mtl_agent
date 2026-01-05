# Ingestion Pipeline

Orchestrates PDF ingestion: parse → extract → embed → store.

## Location

[`ingestor/pipeline.py`](../../ingestor/pipeline.py)

## Class

### `IngestionPipeline`

Pipeline for ingesting product PDFs into vector store.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `parser` | BasePDFParser | - | PDF parser instance (pypdf2 or docling) |
| `extractor` | BaseExtractor | - | LLM extractor for structured data extraction |
| `llm_client` | BaseLLM | - | LLM client with embed() method |
| `vector_store` | BaseVectorStore | - | Vector store for embedding storage |
| `batch_size` | int | 10 | Batch size for embedding generation |

## Methods

### `ingest(source_dir) -> dict`

Ingest all PDFs from source directory.

**Returns:**
| Key | Type | Description |
|-----|------|-------------|
| `total` | int | Total PDF files found |
| `success` | int | Successfully processed |
| `failed` | int | Failed to process |
| `errors` | list | List of error details |

### `ingest_single(pdf_path) -> dict`

Ingest a single PDF file.

**Returns:** Extracted product data with embedding stored.

## Usage

```python
from ingestor.pipeline import IngestionPipeline
from ingestor.extractor.selector import ExtractorSelector
from libs.llm.parser.selector import ParserSelector
from libs.llm.client.selector import LLMClientSelector
from libs.database.vector.selector import VectorStoreSelector

# Create components
parser = ParserSelector.create(provider="docling")
llm_client = LLMClientSelector.create(provider="litellm")
extractor = ExtractorSelector.create(provider="litellm", llm_client=llm_client)
vector_store = VectorStoreSelector.create(provider="qdrant")

# Create pipeline
pipeline = IngestionPipeline(
    parser=parser,
    extractor=extractor,
    llm_client=llm_client,
    vector_store=vector_store,
    batch_size=10
)

# Ingest all PDFs
results = pipeline.ingest("data/product_details")

# Or ingest single file
product = pipeline.ingest_single("data/product_details/1_coffee_maker.pdf")
```

## Dependencies

| Component | Source |
|-----------|--------|
| Parser | `libs/llm/parser/` |
| Extractor | `ingestor/extractor/` |
| LLM Client | `libs/llm/client/` |
| Vector Store | `libs/database/vector/` |
