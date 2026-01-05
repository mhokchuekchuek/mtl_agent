# **📄 Docling Parser**

PDF parsing with layout analysis and markdown output.


---


## **📍 Location**

[`libs/llm/parser/docling/main.py`](../../../../libs/llm/parser/docling/main.py)

---


## **📦 Class**

### `PDFParser`

PDF parser using Docling for structure-preserving extraction.


---


## **📋 Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `**kwargs` | dict | - | Additional configuration for DocumentConverter |

---


## **📋 Methods**


### `parse(pdf_path, **kwargs) -> dict`

Parse PDF and return full content with metadata.

**Returns**:
| Key | Type | Description |
|-----|------|-------------|
| `text` | str | Full extracted text (markdown format) |
| `metadata` | dict | File metadata (filename, filepath, file_size, num_pages, title, author) |
| `pages` | list | List of page dictionaries |

### `parse_pages(pdf_path, **kwargs) -> list[dict]`

Parse PDF and return content organized by page.

**Returns**: List of dictionaries with:
| Key | Type | Description |
|-----|------|-------------|
| `page_number` | int | Page index (0-based) |
| `text` | str | Page text content (markdown format) |
| `metadata` | dict | Page metadata |

---


## **🚀 Usage**

```python
from libs.llm.parser.selector import ParserSelector

parser = ParserSelector.create(provider="docling")

# Parse entire document (markdown output)
result = parser.parse("document.pdf")
print(result["text"])  # Markdown formatted

# Parse page by page
pages = parser.parse_pages("document.pdf")
for page in pages:
    print(f"Page {page['page_number']}: {page['text'][:100]}...")
```

---


## **📝 Notes**

- Preserves document structure (headings, tables, lists)
- Outputs markdown format
- Better for RAG pipelines and chunking
- Slower than PyPDF2
- Reference: https://github.com/DS4SD/docling
