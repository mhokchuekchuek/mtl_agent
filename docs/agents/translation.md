# Translation Agent

Translates text between Thai and English.

## Location

`src/modules/agents/translation/`

## Architecture

```
Input Text
    |
    v
+-------------------+
|  Detect Language  |
+-------------------+
    |
    v
+-------------------+
|  Translate        |
|  (via Langfuse)   |
+-------------------+
    |
    v
Translated Text
```

## Components

### TranslationAgent

Main agent class for language translation.

**Location**: `main.py`

**Inherits**: `BaseAgent`

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `llm_client` | BaseLLM | LLM client for translation |
| `prompt_manager` | BasePromptManager | Prompt manager |
| `prompt_name` | str | Prompt name (default: "translation") |

**Methods**:

| Method | Description |
|--------|-------------|
| `execute(state)` | Execute translation based on state |
| `translate(text, target_lang)` | Translate text to target language |
| `detect_language(text)` | Detect source language |

## Usage

```python
from libs.llm.client.litellm.main import LLMClient
from libs.llm.prompt_manager.langfuse.main import LangfusePromptManager
from src.modules.agents.translation.main import TranslationAgent

# Initialize clients
llm_client = LLMClient(
    proxy_url='http://localhost:4000',
    api_key='sk-1234',
)
prompt_manager = LangfusePromptManager()

# Create agent
agent = TranslationAgent(
    llm_client=llm_client,
    prompt_manager=prompt_manager,
)

# Translate directly
result = agent.translate("สวัสดี", target_lang="en")
# {"translated_text": "Hello", "source_lang": "th", "target_lang": "en"}

# Detect language
lang = agent.detect_language("Hello world")
# "en"

# Execute with state (for LangGraph)
state = {"user_input": "สวัสดี", "target_lang": "en"}
new_state = agent.execute(state)
# {"user_input": "สวัสดี", "translated_text": "Hello", "detected_lang": "th", "target_lang": "en"}
```

## Prompt

**Location**: `prompts/customer_chatbot/translation.prompt`

The prompt provides:
- Translation rules (preserve technical terms)
- Output format (JSON with translated_text and source_lang)
