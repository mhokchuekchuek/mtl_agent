# **🤖 LLM Module**

LLM-related utilities and integrations.


---


## **📍 Location**

`libs/llm/`


---


## **📦 Submodules**

| | | |
|:---:|:---:|:---:|
| [🔗 **Client**](client/README.md)<br/>LLM provider clients | [✂️ **Chunking**](chunking/README.md)<br/>Text chunking strategies | [👁️ **Observability**](observability/README.md)<br/>LLM tracing and monitoring |
| [📄 **Parser**](parser/README.md)<br/>PDF parsing providers | [📝 **Prompt Manager**](prompt_manager/README.md)<br/>Centralized prompt management | |


---


## **🏗️ Architecture**

```text
libs/llm/
├── client/           # LLM provider clients
│   ├── base.py       # BaseLLM abstract class
│   ├── selector.py   # LLMClientSelector
│   ├── litellm/      # HTTP-based client
│   └── langchain/    # ChatOpenAI wrapper
├── chunking/         # Text chunking strategies
│   ├── base.py       # BaseChunker abstract class
│   ├── selector.py   # TextChunkerSelector
│   └── recursive/    # Recursive text splitter
├── observability/    # LLM tracing
│   ├── base.py       # BaseObservability abstract class
│   ├── selector.py   # ObservabilitySelector
│   └── langfuse/     # Langfuse tracing
├── parser/           # PDF parsing
│   ├── base.py       # BasePDFParser abstract class
│   ├── selector.py   # ParserSelector
│   ├── pypdf2/       # Plain text extraction
│   └── docling/      # Markdown extraction
└── prompt_manager/   # Prompt management
    ├── base.py       # BasePromptManager abstract class
    ├── selector.py   # PromptManagerSelector
    └── langfuse/     # Langfuse prompts
```
