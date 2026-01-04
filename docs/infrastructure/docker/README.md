# **🐳 Docker Services**

Docker Compose services for the MTL Agent system.


---


## **📦 Services**

| | | |
|:---:|:---:|:---:|
| [🔴 **Redis**](redis.md)<br/>Port 6379 | [🐘 **PostgreSQL**](postgres.md)<br/>Port 5432 | [🔷 **Qdrant**](qdrant.md)<br/>Ports 6333, 6334 |
| [🤖 **LiteLLM Proxy**](litellm.md)<br/>Port 4000 | [🔗 **API**](api.md)<br/>Port 8000 | [🖥️ **UI**](ui.md)<br/>Port 8501 |


---


## **⚡ Quick Commands**

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


---


## **💾 Data Persistence**

### 📁 **Volumes**

| Volume | Service | Purpose |
|--------|---------|---------|
| `redis_data` | Redis | Cache data |
| `postgres_data` | PostgreSQL | LiteLLM database |
| `qdrant_storage` | Qdrant | Vector embeddings |


### 📂 **Mounted Files**

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./data` | `/app/data` | ERP SQLite database, product PDFs |
| `./configs` | `/app/configs` | Configuration files |
| `./src` | `/app/src` | Application source code |
| `./libs` | `/app/libs` | Shared libraries |


---


## **🌐 Network**

All services are connected via `erp-agent-network` bridge network:

- `redis:6379`
- `postgres:5432`
- `qdrant:6333`
- `litellm-proxy:4000`
- `api:8000`
