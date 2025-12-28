# Why LLM Extractor

## Context

Need to extract structured product data (name, specs, features) from PDF documents.

## Options Considered

| Approach | Pros | Cons |
|----------|------|------|
| Regex/Rule-based | Fast, no API cost | Brittle, breaks on format changes |
| NLP (spaCy, NLTK) | No API cost, good for entities | Limited understanding, manual rules |
| **LLM Extractor** | Flexible, handles varied formats, understands context | API cost, slower |

## Decision

Use LLM extractor.

## Rationale

- Product PDFs have inconsistent formats
- Need to understand context to extract specs/features
- Schema can change without rewriting rules
- Accuracy more important than speed for ingestion
