# Decisions

Architecture and technology decisions for the project.

## General

| Decision | Description |
|----------|-------------|
| [Why Langfuse](why_langfuse.md) | Why use Langfuse for observability, prompt management, and evaluation |

## Ingestor

| Decision | Description |
|----------|-------------|
| [Why PyPDF2 Parser](why_pypdf2_parser.md) | Why use PyPDF2 for PDF parsing |
| [Why LLM Extractor](why_llm_extractor.md) | Why use LLM for data extraction |
| [Why OpenAI Model](why_openai_model.md) | Why use OpenAI GPT-4o-mini |
| [Why Flat Text Payload](why_flat_text_payload.md) | Why store data as flat text instead of structured fields |

## Agents

| Decision | Description |
|----------|-------------|
| [Why ReAct Agent](why_react_agent.md) | Why use ReAct pattern for ProductAgent |
| [Why Checkpointer + Store](why_checkpointer_and_store.md) | Why use both Redis Checkpointer and Postgres Store for memory |
