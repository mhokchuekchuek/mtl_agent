# **🔗 API**

FastAPI application serving the ERP multi-agent system.


---


## **⚙️ Configuration**

```yaml
api:
  build:
    context: .
    dockerfile: docker/api/Dockerfile
  ports:
    - "8000:8000"
```


---


## **📋 Details**

| Property | Value |
|----------|-------|
| Port | 8000 |
| Dockerfile | `docker/api/Dockerfile` |
| Docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |


---


## **💡 Purpose**

- Serve ERP agent API endpoints
- Handle query requests
- Orchestrate multi-agent workflow


---


## **🚀 Commands**

```bash
# Build
docker-compose build api

# Start
docker-compose up -d api

# Rebuild and start
docker-compose up -d --build api

# View logs
docker-compose logs -f api
```
