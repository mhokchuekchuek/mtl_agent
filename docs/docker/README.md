# Docker Services

Docker Compose services for the MTL Agent system.

## Services

| Service | Port | Documentation |
|---------|------|---------------|
| Redis | 6379 | [redis.md](redis.md) |
| PostgreSQL | 5432 | [postgres.md](postgres.md) |
| Qdrant | 6333, 6334 | [qdrant.md](qdrant.md) |
| LiteLLM Proxy | 4000 | [litellm.md](litellm.md) |
| API | 8000 | [api.md](api.md) |
| UI | 8501 | [ui.md](ui.md) |

## Quick Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Clean restart (removes data)
docker-compose down -v && docker-compose up -d
```

## Data Persistence

### Volumes

| Volume | Service | Purpose |
|--------|---------|---------|
| `redis_data` | Redis | Cache data |
| `postgres_data` | PostgreSQL | LiteLLM database |
| `qdrant_storage` | Qdrant | Vector embeddings |

### Mounted Files

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./data` | `/app/data` | ERP SQLite database, product PDFs |
| `./configs` | `/app/configs` | Configuration files |
| `./src` | `/app/src` | Application source code |
| `./libs` | `/app/libs` | Shared libraries |

## Network

All services are connected via `erp-agent-network` bridge network:

- `redis:6379`
- `postgres:5432`
- `qdrant:6333`
- `litellm-proxy:4000`
- `api:8000`
