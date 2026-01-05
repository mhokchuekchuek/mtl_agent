# LiteLLM Extractor

LLM-based structured data extraction using LiteLLM client.

## Location

[`ingestor/extractor/litellm/main.py`](../../../ingestor/extractor/litellm/main.py)

## Class

### `LLMExtractor`

Extract structured product data using LLM.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `llm_client` | BaseLLM | Yes | LLM client instance for text generation |
| `prompt` | Langfuse Prompt | Yes | Prompt object with `compile()` method |
| `**kwargs` | dict | No | Additional arguments |

## Methods

### `extract(text, **kwargs) -> dict`

Extract structured product data from text.

**Returns:**
| Key | Type | Description |
|-----|------|-------------|
| `product_name` | str | Product name from title |
| `description` | str | Description paragraph |
| `specifications` | dict | Key-value pairs of specs |
| `features` | list[dict] | List of `{title, description}` |
| `summary` | str | Closing summary paragraph |

## Usage

```python
from ingestor.extractor.selector import ExtractorSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.prompt_manager.selector import PromptManagerSelector

# Create LLM client
llm_client = LLMClientSelector.create(
    provider="litellm",
    proxy_url="http://localhost:4000",
    api_key="sk-...",
    completion_model="gpt-4o-mini"
)

# Create prompt manager and fetch prompt
prompt_manager = PromptManagerSelector.create(
    provider="langfuse",
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"
)
prompt = prompt_manager.get_prompt("ingestor_extract_product", label="latest")

# Create extractor with injected prompt
extractor = ExtractorSelector.create(
    provider="litellm",
    llm_client=llm_client,
    prompt=prompt
)

# Extract from text
result = extractor.extract(pdf_text, product_id=123)
print(result["product_name"])
print(result["specifications"])
```

## Output Example

```json
{
  "product_name": "Espresso Coffee Maker",
  "description": "Premium espresso machine for home use...",
  "specifications": {
    "product_type": "Coffee Maker",
    "category": "Kitchen Appliances",
    "dimensions": "12 x 8 x 14 inches",
    "weight": "10 lbs"
  },
  "features": [
    {
      "title": "15-Bar Pump",
      "description": "Professional-grade pressure for rich espresso"
    }
  ],
  "summary": "The perfect addition to your kitchen..."
}
```

## Prompt

The prompt is injected from the caller. Typically fetched from Langfuse using `prompt_manager.get_prompt()`. Ensure the `ingestor_extract_product` prompt is uploaded before running extraction. See [Prompts Documentation](../../prompts/README.md).

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Empty text | Raises `ValueError` |
| Invalid JSON response | Returns empty fields with `_parse_error: true` |
| LLM timeout | Raises exception from LLM client |
