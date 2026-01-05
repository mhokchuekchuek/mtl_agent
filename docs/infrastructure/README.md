# **🔧 Infrastructure**

Infrastructure documentation for running the MTL ERP Assistant.


---


## **📋 Overview**

```
infrastructure/
├── docker/           # Docker container configurations
│   ├── README.md
│   ├── api.md
│   ├── litellm.md
│   ├── postgres.md
│   ├── qdrant.md
│   ├── redis.md
│   └── ui.md
└── setup/            # Development environment setup
    ├── README.md
    └── local/        # Local development setup
        ├── README.md
        ├── prerequisites.md
        ├── environment.md
        └── troubleshooting.md
```

> 📝 **Note:** Database documentation moved to [docs/database/](../database/README.md).


---


## **🚀 Quick Start**

> ⚠️ **Important:** Complete these steps in order.

1. [Prerequisites](setup/local/prerequisites.md) - Required software
2. [Environment Setup](setup/local/environment.md) - Configure environment variables
3. [Docker Services](docker/README.md) - Start containers
4. [Databases](../database/README.md) - Database schemas


---


## **🐳 Services**

| Service | Port | Purpose |
|---------|------|---------|
| API | 8000 | FastAPI backend |
| Customer UI | 8501 | Streamlit customer chatbot |
| Client UI | 8502 | Streamlit BI analytics |
| LiteLLM Proxy | 4000 | LLM gateway |
| PostgreSQL | 5432 | Long-term memory store |
| Redis | 6379 | Short-term memory (checkpointer) |
| Qdrant | 6333 | Vector database |


---


## **⌨️ Commands**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```
