# CLI (main.py)

Application CLI for running API and UI locally.

## Commands

| Command | Purpose | Documentation |
|---------|---------|---------------|
| api | Start FastAPI REST API server | [api.md](api.md) |
| ui | Start Streamlit web UI | [ui.md](ui.md) |

## Quick Start

```bash
# Start API server
python main.py api

# Start Streamlit UI
python main.py ui
```

## Docker

When using Docker, services are started via `docker-compose`:

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api
docker-compose up -d ui
```

## Local Development

For local development without Docker:

```bash
# Terminal 1: Start API
python main.py api --reload

# Terminal 2: Start UI
python main.py ui
```
