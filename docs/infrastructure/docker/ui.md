# **🖥️ UI Services**

Streamlit web interfaces for the MTL ERP Assistant.


---


## **📋 Containers**

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| Customer UI | `erp-agent-customer-ui` | 8501 | Customer support chatbot |
| Client UI | `erp-agent-client-ui` | 8502 | BI analytics chatbot |


---


## **🚀 Commands**

```bash
# Start UI services
docker-compose up -d customer-ui client-ui

# View logs
docker-compose logs -f customer-ui
docker-compose logs -f client-ui

# Restart
docker-compose restart customer-ui client-ui
```


---


## **🔑 Environment Variables**

| Variable | Description |
|----------|-------------|
| `API_BASE_URL` | API service URL (default: `http://api:8000`) |


---


## **📂 Volumes**

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./ui` | `/app/ui` | UI source code |
| `./configs` | `/app/configs:ro` | Configuration (read-only) |


---


## **🔗 Dependencies**

- `api` - REST API service


---


## **🌐 Access**

| UI | URL |
|----|-----|
| Customer Support | http://localhost:8501 |
| BI Analytics | http://localhost:8502 |


---


## **🛠️ Technology Stack**

- **Streamlit** - Python web app framework
- **Requests** - HTTP client for API calls


---


## **🏗️ Architecture**

```
ui/
├── __init__.py
├── customer_app.py    # Customer support chatbot UI
└── client_app.py      # BI analytics chatbot UI
```


---


## **✨ Features**


### 👤 **Customer UI** (`customer_app.py`)

- Product search and recommendations
- Order placement and cancellation
- Stock and price inquiries
- Thai/English support


### 💼 **Client UI** (`client_app.py`)

- BI analytics queries
- Data visualization (Plotly charts)
- Customer chat history lookup
- Intent classification display
