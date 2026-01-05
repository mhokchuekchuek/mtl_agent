# **📄 Product PDFs**

PDF files containing detailed product information for the RAG knowledge base.


---


## **📍 Location**

[`data/product_details/`](../../data/product_details/)


---


## **📋 Overview**

100 PDF files, each containing detailed information about a product.


---


## **📂 Structure**

Each PDF contains:
- Product name and overview
- Technical specifications
- Features and descriptions
- 2 pages per product


---


## **💡 Usage**

These PDFs are processed by the [Ingestor Pipeline](../ingestor/README.md) to:
1. Parse PDF content using PyPDF2
2. Extract structured data via LLM (gpt-4o-mini)
3. Generate embeddings using text-embedding-3-small
4. Store in Qdrant vector database

> 📝 **Note:** The ProductAgent uses these embeddings for semantic product search.


---


## **⚙️ Configuration**

See `configs/ingestor/settings.yaml`:

```yaml
ingestor:
  parser: pypdf2
  pdf_dir: data/product_details
  batch_size: 10
  llm:
    embedding_model: text-embedding-3-small
```
