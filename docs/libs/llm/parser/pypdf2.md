# **📄 PyPDF2 Parser**

Plain text extraction using PyPDF2 library.


---


## **📍 Location**

[`libs/llm/parser/pypdf2/main.py`](../../../../libs/llm/parser/pypdf2/main.py)

---


## **📦 Class**

### `PDFParser`

PDF parser using PyPDF2 for simple text extraction.


---


## **📋 Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `**kwargs` | dict | - | Additional configuration (currently unused) |

---


## **📋 Methods**


### `parse(pdf_path, **kwargs) -> dict`

Parse PDF and return full content with metadata.

**Returns**:
| Key | Type | Description |
|-----|------|-------------|
| `text` | str | Full extracted text (all pages combined) |
| `metadata` | dict | File metadata (filename, filepath, file_size, num_pages, title, author) |
| `pages` | list | List of page dictionaries |

### `parse_pages(pdf_path, **kwargs) -> list[dict]`

Parse PDF and return content organized by page.

**Returns**: List of dictionaries with:
| Key | Type | Description |
|-----|------|-------------|
| `page_number` | int | Page index (0-based) |
| `text` | str | Page text content |
| `metadata` | dict | Page metadata |

---


## **🚀 Usage**

```python
from libs.llm.parser.selector import ParserSelector

parser = ParserSelector.create(provider="pypdf2")

# Parse entire document
result = parser.parse("document.pdf")
print(result["text"])
print(result["metadata"]["num_pages"])

# Parse page by page
pages = parser.parse_pages("document.pdf")
for page in pages:
    print(f"Page {page['page_number']}: {page['text'][:100]}...")
```

---


## **📝 Notes**

- Fast and lightweight
- Loses document structure (headings, tables, lists)
- Best for simple text extraction or large batches
