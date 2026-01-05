# **⚙️ Ingestor**

Data ingestion pipeline for processing product PDFs into vector embeddings.


---


## **📑 Table of Contents**

- [Location](#-location)
- [Submodules](#-submodules)
- [Architecture](#-architecture)
- [Pipeline Flow](#-pipeline-flow)
- [Configuration](#-configuration)
- [Script](#-script)


---


## **📍 Location**

[`ingestor/`](../../ingestor/)


---


## **📦 Submodules**

| | |
|:---:|:---:|
| [📄 **Product PDFs**](product-pdfs.md)<br/>100 product detail PDF files | [🔍 **Extractor**](extractor/README.md)<br/>LLM-based structured data extraction |
| [🔄 **Pipeline**](pipeline.md)<br/>Orchestration of parse → extract → embed → store | |


---


## **🔗 Related**

- [Decisions](../decisions/README.md) - Architecture and technology decisions
- [Future Improvements](../future_improvements/ingestion/workflow_orchestrator.md) - Production enhancements
- [Why Langfuse](../decisions/why_langfuse.md) - Observability and prompt management


---


## **🏗️ Architecture**

```text
ingestor/
├── pipeline.py         # Main ingestion pipeline
└── extractor/          # LLM extraction providers
    ├── base.py         # BaseExtractor abstract class
    ├── selector.py     # ExtractorSelector
    └── litellm/        # LiteLLM provider
        └── main.py
```


---


## **🔄 Pipeline Flow**

```mermaid
flowchart LR
    subgraph Input
        PDF[PDF Files]
    end

    subgraph Parse
        Parser[PDF Parser<br/>PyPDF2/Docling]
    end

    subgraph Extract
        LLM[LLM Extractor<br/>gpt-4o-mini]
        Prompt[Langfuse Prompt<br/>ingestor_extract_product]
    end

    subgraph Embed
        Embedder[Embedding Model<br/>text-embedding-3-small]
    end

    subgraph Store
        Qdrant[(Qdrant<br/>Vector DB)]
    end

    PDF --> Parser
    Parser -->|markdown/text| LLM
    Prompt -.->|inject| LLM
    LLM -->|structured JSON| Embedder
    Embedder -->|vectors| Qdrant
```

| Stage | Description | Details |
|-------|-------------|---------|
| Parse | Turn PDF to markdown/text format | PyPDF2 or Docling |
| Extract | Extract structured product data via LLM | [how_it_works.md](extractor/how_it_works.md) |
| Embed | Generate vector embeddings from content | text-embedding-3-small |
| Store | Save embeddings and metadata to Qdrant | With product metadata |


---


## **📤 Output**

Data stored in Qdrant with payload containing `product_id`, `product_name`, `source_file`, and `text` (combined description + attributes for semantic search).


---


## **🔌 Dependencies**

> ⚠️ **Important:** Langfuse prompts must be uploaded before running ingestion.

Prompts are retrieved from Langfuse at runtime. Ensure the `ingestor_extract_product` prompt is uploaded. See [Prompts Documentation](../prompts/README.md).


---


## **⚙️ Configuration**

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


### 🔧 **Options**

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


### 🌍 **Environment Overrides**

```bash
INGESTOR__PARSER=pypdf2 python scripts/ingest_pdfs.py
```


---


## **▶️ Script**

**Location**: `scripts/ingest_pdfs.py`

```bash
python scripts/ingest_pdfs.py
```
