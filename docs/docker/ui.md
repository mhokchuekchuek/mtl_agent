# UI Service

ReactPy web interface for the MTL ERP Assistant.

## Container

| Property | Value |
|----------|-------|
| Image | Built from `docker/ui/Dockerfile` |
| Container | `erp-agent-ui` |
| Port | 8501 |

## Commands

```bash
# Start UI service
docker-compose up -d ui

# View logs
docker-compose logs -f ui

# Restart
docker-compose restart ui
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `API_URL` | API service URL (default: `http://localhost:8000`) |

## Volumes

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./ui` | `/app/ui` | UI source code |
| `./configs` | `/app/configs` | Configuration |

## Dependencies

- `api` - REST API service

## Access

http://localhost:8501

## Technology Stack

- **ReactPy** - Python reactive UI framework
- **FastAPI** - ASGI web framework
- **Uvicorn** - ASGI server

## Architecture

```
ui/
├── app.py               # Main ReactPy application
├── server.py            # FastAPI + ReactPy server
├── api_client.py        # HTTP client for backend API
├── config.py            # Configuration (API_BASE_URL, endpoints)
├── state.py             # AppState dataclass
├── styles.py            # CSS constants and style dicts
└── components/          # ReactPy components
    ├── header.py
    ├── sidebar.py
    ├── chat_area.py
    ├── message_bubble.py
    ├── typing_indicator.py
    └── new_chat_modal.py
```
