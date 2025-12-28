# Prompt Management

Centralized prompt management using [Langfuse](../decisions/why_langfuse.md).

## Overview

Prompts are stored as `.prompt` files with YAML frontmatter and uploaded to Langfuse for:
- Version control
- A/B testing
- Centralized management
- Runtime retrieval

## Architecture

```
prompts/                          # Local .prompt files
    └── uploader.py               # PromptUploader class
        ↓
libs/llm/prompt_manager/          # Prompt manager abstraction
    ├── base.py                   # BasePromptManager ABC
    ├── selector.py               # PromptManagerSelector
    └── langfuse/main.py          # LangfusePromptManager
        ↓
Langfuse Cloud                    # Centralized storage
```

## Prompt File Format

`.prompt` files use YAML frontmatter with template content:

```yaml
---
name: extract_product
model: gpt-4o-mini
description: Extract structured product information
input_schema:
  type: object
  properties:
    text:
      type: string
      description: Raw text content
  required:
    - text
output_schema:
  type: object
  properties:
    product_name:
      type: string
---
You are a product data extractor...

## Input:
{{text}}

## Output:
Return JSON with product_name, description, etc.
```

### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Prompt identifier |
| `model` | Target LLM model |
| `description` | What the prompt does |
| `input_schema` | JSON Schema for input variables |
| `output_schema` | JSON Schema for expected output |

### Template Variables

Use `{{variable_name}}` for variable substitution.

## Configuration

**File:** `configs/prompts/settings.yaml`

```yaml
prompt_manager:
  directory: prompts
  version: "v1"
  label: "latest"

  langfuse:
    enabled: true
    provider: langfuse
    host: "@format {env[LANGFUSE_BASE_URL]}"
    public_key: "@format {env[LANGFUSE_PUBLIC_KEY]}"
    secret_key: "@format {env[LANGFUSE_SECRET_KEY]}"
```

### Options

| Key | Description | Default |
|-----|-------------|---------|
| `prompt_manager.directory` | Directory containing .prompt files | `prompts` |
| `prompt_manager.version` | Version tag for uploaded prompts | `v1` |
| `prompt_manager.label` | Label for prompt retrieval | `latest` |
| `prompt_manager.langfuse.host` | Langfuse host URL | From `LANGFUSE_BASE_URL` |
| `prompt_manager.langfuse.public_key` | Langfuse public key | From `LANGFUSE_PUBLIC_KEY` |
| `prompt_manager.langfuse.secret_key` | Langfuse secret key | From `LANGFUSE_SECRET_KEY` |

See [Dynaconf docs](../libs/configs/dynaconf.md) for `@format` environment variable syntax.

## Upload Prompts to Langfuse

```bash
# Ensure .env has Langfuse keys, then run:
python scripts/upload_prompts.py
```

## Usage in Code

### Retrieve Prompt

```python
from libs.llm.prompt_manager.selector import PromptManagerSelector

# Create prompt manager
pm = PromptManagerSelector.create(provider="langfuse")

# Get prompt from Langfuse
prompt = pm.get_prompt("ingestor_extract_product")

# Compile with variables
compiled = prompt.compile(text="Product description...")
```

### Upload Prompt Programmatically

```python
from prompts.uploader import PromptUploader

uploader = PromptUploader()
count = uploader.process()  # Uploads all .prompt files
```

## Prompt Naming Convention

Prompts are named based on directory structure:

| File Path | Prompt Name |
|-----------|-------------|
| `prompts/ingestor/extract_product.prompt` | `ingestor_extract_product` |
| `prompts/supervisor/classify_query.prompt` | `supervisor_classify_query` |
| `prompts/sql_agent/generate_sql.prompt` | `sql_agent_generate_sql` |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Langfuse public API key |
| `LANGFUSE_SECRET_KEY` | Langfuse secret API key |
| `LANGFUSE_HOST` | Langfuse host (default: cloud) |
