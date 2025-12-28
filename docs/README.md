# MTL Agent Documentation

Documentation for the MTL Agent ERP multi-agent system.

## Architecture

| Section | Purpose | Documentation |
|---------|---------|---------------|
| Architecture | Code architecture and layers | [architecture/](architecture/README.md) |
| Decisions | Architecture decision records | [decisions/](decisions/README.md) |

## Application Layers

| Layer | Purpose | Documentation |
|-------|---------|---------------|
| Dependencies | DI wiring (`build_*_service`) | [dependencies/](dependencies/README.md) |
| Usecases | Business logic orchestration | [usecases/](usecases/README.md) |
| Repositories | Chatbots, checkpointers, stores | [repositories/](repositories/README.md) |

## Modules

| Module | Purpose | Documentation |
|--------|---------|---------------|
| Agents | LLM-powered agents | [agents/](agents/README.md) |
| Tools | LangChain tools for agents | [tools/](tools/README.md) |
| Workflows | LangGraph workflows (uncompiled) | [workflows/](workflows/README.md) |

## Infrastructure

| Section | Purpose | Documentation |
|---------|---------|---------------|
| Libs | Reusable infrastructure (cross-project) | [libs/](libs/README.md) |
| Docker | Docker services | [docker/](docker/README.md) |
| Setup | Installation and configuration | [setup/](setup/README.md) |

## Data & Prompts

| Section | Purpose | Documentation |
|---------|---------|---------------|
| Prompts | Prompt management with Langfuse | [prompts/](prompts/README.md) |
| Data Sources | ERP database, product PDFs | [data-sources/](data-sources/README.md) |
| Ingestor | PDF ingestion pipeline | [ingestor/](ingestor/README.md) |

## API

| Section | Purpose | Documentation |
|---------|---------|---------------|
| API Overview | REST API architecture | [api/](api/README.md) |
| Routes | API endpoints | [api/routes.md](api/routes.md) |

## Other

| Section | Purpose | Documentation |
|---------|---------|---------------|
| CLI | Command-line interface | [cli/](cli/README.md) |
| Future Improvements | Potential enhancements | [future_improvements/](future_improvements/README.md) |
