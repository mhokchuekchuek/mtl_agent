# **🔍 Search Algorithms**

**Current**: Default HNSW dense vector search

**Improvement**: Hybrid search combining dense and sparse vectors


---


## **📊 Options**

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| HNSW | Graph-based dense vector index, fast and accurate | General semantic search |
| Sparse Vectors | Inverted index for keyword matching | Exact term matching |
| [Hybrid Search](https://qdrant.tech/articles/hybrid-search/) | Combines dense + sparse with RRF fusion | Best of both worlds |
| [ColBERT Reranking](https://qdrant.tech/documentation/advanced-tutorials/reranking-hybrid-search/) | Multi-vector reranking after initial retrieval | Maximum relevance |
