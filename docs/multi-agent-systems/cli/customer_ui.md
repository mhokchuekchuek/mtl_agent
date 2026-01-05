# **👤 customer_ui**

Start Customer Support Streamlit UI.


---


## **🚀 Usage**

```bash
python main.py customer_ui [OPTIONS]
```


---


## **⚙️ Options**

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--host` | `-h` | `0.0.0.0` | Host to bind |
| `--port` | `-p` | `8501` | Port to bind |


---


## **💡 Examples**

```bash
# Default (0.0.0.0:8501)
python main.py customer_ui

# Custom port
python main.py customer_ui --port 8503

# Localhost only
python main.py customer_ui --host 127.0.0.1
```


---


## **🐳 Docker**

```bash
docker-compose up -d customer-ui
```

Access at: http://localhost:8501


---


## **⚡ Streamlit App**

The UI is launched via subprocess:

```python
subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    "ui/customer_app.py",
    "--server.address", host,
    "--server.port", str(port),
    "--server.headless", "true",
])
```


---


## **✨ Features**

| Feature | Description |
|---------|-------------|
| Product Search | Search products by name, category |
| Order Management | Place orders, cancel orders, view order status |
| Chat History | Conversation memory within session |
| Thai Support | Full Thai language support |



