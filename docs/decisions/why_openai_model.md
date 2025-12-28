# Why OpenAI Model

## Context

Need to choose an LLM model for structured data extraction from product PDFs.

## Options Considered

| Model | Pros | Cons |
|-------|------|------|
| **GPT-4o-mini** | Good accuracy, fast, low cost | API dependency |
| GPT-4o | Best accuracy | Higher cost |
| Local (Llama, Mistral) | No API cost, private | Cannot run on M2 Mac |

## Decision

Use GPT-4o-mini.

## Rationale

- Low cost (this is an assignment project)
- Local LLMs cannot run on M2 Mac hardware
