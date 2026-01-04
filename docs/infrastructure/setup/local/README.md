# **💻 Local Development Setup**

Development environment using Docker Compose.


---


## **📑 Table of Contents**

- [Documentation](#-documentation)
- [Quick Start](#-quick-start)
- [Verify Installation](#-verify-installation)
- [Access Services](#-access-services)


---


## **📖 Documentation**

| | | |
|:---:|:---:|:---:|
| [📋 **Prerequisites**](prerequisites.md)<br/>Required software and tools | [🔐 **Environment**](environment.md)<br/>Environment variables | [🔧 **Troubleshooting**](troubleshooting.md)<br/>Common issues and solutions |


---


## **🚀 Quick Start**

### 1️⃣ **Setup Environment**

```bash
cp .env.template .env
# Edit .env with your API keys (OPENAI_API_KEY required)
```


### 2️⃣ **Start Docker Services**

```bash
docker-compose up -d
docker-compose ps
```

This starts:
- PostgreSQL (port 5432) - Long-term memory store
- Redis (port 6379) - Short-term memory checkpointer
- Qdrant (port 6333) - Vector database
- LiteLLM Proxy (port 4000) - LLM gateway


### 3️⃣ **Install Python Dependencies**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```


### 4️⃣ **Run Database Migrations**

```bash
./scripts/run_migrations.sh
```

This adds required columns (e.g., `status` on Orders table) to the SQLite database.


### 5️⃣ **Ingest Knowledge Base**

```bash
python scripts/ingest_pdfs.py
```


### 6️⃣ **Upload Prompts**

Required for first-time setup or when updating prompts:

```bash
python prompts/uploader.py
```


### 7️⃣ **Run Application**

**API Server:**

```bash
uvicorn src.api.main:app --reload --port 8000
```

**Streamlit UI:**

```bash
streamlit run ui/customer_app.py --server.port 8501
streamlit run ui/client_app.py --server.port 8502
```


---


## **✅ Verify Installation**

```bash
curl http://localhost:8000/health
# {"status": "healthy", "service": "erp-agent"}
```


---


## **🔗 Access Services**

| Service | URL |
|---------|-----|
| API Server | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Customer UI | http://localhost:8501 |
| Client UI | http://localhost:8502 |
| LiteLLM Proxy | http://localhost:4000 |
| Qdrant Dashboard | http://localhost:6333/dashboard |
