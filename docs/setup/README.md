# Setup Guide

Installation and configuration guide for the MTL Agent system.

## Sections

| Section | Description | Documentation |
|---------|-------------|---------------|
| Prerequisites | Required software and tools | [prerequisites.md](prerequisites.md) |
| Environment | Environment variables configuration | [environment.md](environment.md) |
| Troubleshooting | Common issues and solutions | [troubleshooting.md](troubleshooting.md) |

## Quick Start

### 1. Setup Environment

```bash
cp .env.template .env
# Edit .env with your API keys (OPENAI_API_KEY required)
```

### 2. Start Docker Services

```bash
docker-compose up -d
docker-compose ps
```

### 3. Install Python Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 4. Ingest Knowledge Base

```bash
python scripts/ingest_pdfs.py
```

### 5. Upload Prompts (Optional)

Only needed when adding or updating prompt templates:

```bash
python scripts/upload_prompts.py
```

## Verify Installation

```bash
curl http://localhost:8000/health
# {"status": "healthy", "service": "erp-agent"}
```
