# Product PDFs

PDF files containing detailed product information for the RAG knowledge base.

## Location

`data/product_details/`

## Overview

100 PDF files, each containing detailed information about a product.

## Structure

Each PDF contains:
- Product name and overview
- Technical specifications
- Features and descriptions
- 2 pages per product

## Usage

These PDFs are processed by the ingestion pipeline (Task 04) to:
1. Extract text content using pdfplumber
2. Chunk text into smaller segments
3. Generate embeddings using fastembed
4. Store in Qdrant vector database

The RAG agent uses these embeddings to answer product-related questions.
