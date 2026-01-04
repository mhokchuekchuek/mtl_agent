# **💼 client_ui**

Start Client BI Analytics Streamlit UI.


---


## **🚀 Usage**

```bash
python main.py client_ui [OPTIONS]
```


---


## **⚙️ Options**

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--host` | `-h` | `0.0.0.0` | Host to bind |
| `--port` | `-p` | `8502` | Port to bind |


---


## **💡 Examples**

```bash
# Default (0.0.0.0:8502)
python main.py client_ui

# Custom port
python main.py client_ui --port 8503

# Localhost only
python main.py client_ui --host 127.0.0.1
```


---


## **🐳 Docker**

```bash
docker-compose up -d client-ui
```

Access at: http://localhost:8502


---


## **⚡ Streamlit App**

The UI is launched via subprocess:

```python
subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    "ui/client_app.py",
    "--server.address", host,
    "--server.port", str(port),
    "--server.headless", "true",
])
```


---


## **✨ Features**

| Feature | Description |
|---------|-------------|
| SQL Analytics | Query business data with natural language |
| Visualization | Generate Plotly charts from data |
| Customer Chat History | Lookup customer conversation history |
| Insights | Business intelligence insights |
| Thai Support | Full Thai language support |


---


## **🔗 Full Code**

See [`main.py`](../../../main.py) - `client_ui` command
