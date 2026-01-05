# **📄 Parser**

PDF parsing providers using the provider/selector pattern.


---


## **📍 Location**

[`libs/llm/parser/`](../../../../libs/llm/parser/)


---


## **📦 Providers**

| | |
|:---:|:---:|
| [📝 **PyPDF2**](pypdf2.md)<br/>Plain text extraction, fast and lightweight | [📋 **Docling**](docling.md)<br/>Markdown output with layout analysis |


---


## **🔧 Classes**


### 🎯 **BasePDFParser**

Abstract base class for PDF parsers.

**Location**: `libs/llm/parser/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `parse(pdf_path, **kwargs)` | Parse PDF and return text, metadata, and pages |
| `parse_pages(pdf_path, **kwargs)` | Parse PDF and return content organized by page |


### 🔀 **ParserSelector**

Selector for PDF parser providers.

**Location**: `libs/llm/parser/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create parser instance |
| `list_providers()` | List available providers |
