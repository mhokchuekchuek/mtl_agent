# ERP Multi-Agent System

AI-powered ERP assistant using LiteLLM, LangGraph, and Qdrant for product/order queries.

## Features

- **Natural Language Queries**: Ask questions about products, orders, inventory
- **SQL Generation**: Convert natural language to SQL for ERP database
- **Knowledge Base Search**: Hybrid search (semantic + BM25) on product PDFs
- **Multi-Agent Architecture**: Specialized agents for different query types

## Tech Stack

| Category | Technology |
|----------|------------|
| LLM Router | LiteLLM (OpenAI-compatible) |
| Agent Orchestration | LangGraph |
| Vector Database | Qdrant (hybrid search) |
| API Framework | FastAPI |
| Configuration | Dynaconf |
| Observability | Langfuse |
| Databases | SQLite (ERP), PostgreSQL (memory store) |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- OpenAI API key

### Setup

```bash
# 1. Setup environment
cp .env.template .env
# Edit .env with your OPENAI_API_KEY

# 2. Install dependencies
python -m venv .venv  # first time only
source .venv/bin/activate
pip install -r requirements.txt

# 3. Start services (includes API and UI)
docker-compose up -d

# 4. Run database migrations
./scripts/run_migrations.sh

# 5. Ingest knowledge base
python scripts/ingest_pdfs.py

# 6. Upload prompts (optional)
python scripts/upload_prompts.py
```

> For detailed setup instructions, see [docs/setup/README.md](docs/setup/README.md).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | [`/api/v1/chatbot/customer/chat`](docs/api/endpoints/customer-chat.md) | Customer chatbot (product inquiries) |
| POST | [`/api/v1/chatbot/client/chat`](docs/api/endpoints/client-chat.md) | Client chatbot (internal BI) |

For full API documentation, see [docs/api/README.md](docs/api/README.md).

### Example

```bash
# Customer chatbot
curl -X POST http://localhost:8000/api/v1/chatbot/customer/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "สินค้าประกันชีวิตมีอะไรบ้าง", "thread_id": "test-123"}'

# Client chatbot (internal BI)
curl -X POST http://localhost:8000/api/v1/chatbot/client/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "แสดงยอดขายรายเดือน", "thread_id": "test-456"}'
```

## Project Structure

```
├── src/
│   ├── api/            # HTTP endpoints (routes, schemas)
│   ├── dependencies/   # DI wiring (build_*_service)
│   ├── usecases/       # Business logic (ChatbotService)
│   ├── repositories/   # Data access (chatbots, checkpointers, stores)
│   └── modules/
│       ├── agents/     # AI agents (Translation, Product, Client)
│       ├── tools/      # LangChain tools (SQL, VectorDB, Visualization)
│       └── workflows/  # LangGraph workflows
├── libs/               # Reusable infrastructure (cross-project)
└── configs/            # Configuration files
```

## Documentation

Full documentation available at [docs/README.md](docs/README.md).
