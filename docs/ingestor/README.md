# Ingestor

Data ingestion pipeline for processing product PDFs into vector embeddings.

## Location

`ingestor/`

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| Extractor | LLM-based structured data extraction | [extractor/README.md](extractor/README.md) |
| Pipeline | Orchestration of parse → extract → embed → store | [pipeline.md](pipeline.md) |

## Related

- [Decisions](../decisions/#ingestor) - Architecture and technology decisions
- [Future Improvements](../future_improvements/#ingestor) - Production enhancements
- [Why Langfuse](../decisions/why_langfuse.md) - Observability and prompt management

## Architecture

```text
ingestor/
├── pipeline.py         # Main ingestion pipeline
└── extractor/          # LLM extraction providers
    ├── base.py         # BaseExtractor abstract class
    ├── selector.py     # ExtractorSelector
    └── litellm/        # LiteLLM provider
        └── main.py
```

## Pipeline Flow

| Stage | Description | Details |
|-------|-------------|---------|
| Parse | Turn PDF to markdown/text format | |
| Extract | Extract structured product data via LLM | [how_it_works.md](extractor/how_it_works.md) |
| Embed | Generate vector embeddings from content | |
| Store | Save embeddings and metadata to Qdrant | |

```text
┌─────────────┐     ┌───────────────┐     ┌─────────────┐     ┌────────────────┐     ┌─────────────┐
│  Raw Text   │ --> │ Build Prompt  │ --> │  Call LLM   │ --> │ Parse Response │ --> │ Structured  │
│  (from PDF) │     │ (text+schema) │     │(GPT-4o-mini)│     │ (extract JSON) │     │    Data     │
└─────────────┘     └───────────────┘     └─────────────┘     └────────────────┘     └─────────────┘
```

## Output

Data stored in Qdrant with payload containing `product_id`, `product_name`, `source_file`, and `text` (combined description + attributes for semantic search).

![Ingestor Output](../assets/ingestor_output.png)

## Dependencies

- **Langfuse**: Prompts are retrieved from Langfuse at runtime. Ensure the `ingestor_extract_product` prompt is uploaded before running ingestion. See [Prompts Documentation](../prompts/README.md).

## Configuration

**Location**: `configs/ingestor/settings.yaml`

```yaml
ingestor:
  parser: pypdf2           # pypdf2 | docling
  pdf_dir: data/product_details
  batch_size: 10

  qdrant:
    host: localhost
    port: 6333
    collection: products
    vector_size: 1536

  llm:
    proxy_url: http://localhost:4000
    api_key: "@format {env[LITELLM_MASTER_KEY]}"
    completion_model: gpt-4o-mini
    embedding_model: text-embedding-3-small

  prompts:
    extractor:
      name: ingestor_extract_product
      label: latest
```

### Options

| Key | Description | Default |
|-----|-------------|---------|
| `ingestor.parser` | PDF parser (`pypdf2`, `docling`) | `pypdf2` |
| `ingestor.pdf_dir` | PDF source directory | `data/product_details` |
| `ingestor.batch_size` | Embedding batch size | `10` |
| `ingestor.qdrant.host` | Qdrant hostname | `localhost` |
| `ingestor.qdrant.port` | Qdrant port | `6333` |
| `ingestor.qdrant.collection` | Collection name | `products` |
| `ingestor.qdrant.vector_size` | Vector dimension | `1536` |
| `ingestor.llm.proxy_url` | LiteLLM proxy URL | `http://localhost:4000` |
| `ingestor.llm.api_key` | LiteLLM API key | From `LITELLM_MASTER_KEY` |
| `ingestor.llm.completion_model` | Extraction model | `gpt-4o-mini` |
| `ingestor.llm.embedding_model` | Embedding model | `text-embedding-3-small` |
| `ingestor.prompts.extractor.name` | Langfuse prompt name | `ingestor_extract_product` |
| `ingestor.prompts.extractor.label` | Prompt label | `latest` |

### Environment Overrides

```bash
INGESTOR__PARSER=pypdf2 python scripts/ingest_pdfs.py
```

## Script

**Location**: `scripts/ingest_pdfs.py`

```bash
python scripts/ingest_pdfs.py
```
