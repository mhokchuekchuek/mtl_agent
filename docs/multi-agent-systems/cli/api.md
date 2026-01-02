# api

Start FastAPI REST API server.

## Usage

```bash
python main.py api [OPTIONS]
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--host` | `-h` | `0.0.0.0` | Host to bind |
| `--port` | `-p` | `8000` | Port to bind |
| `--reload` | `-r` | `false` | Enable auto-reload |

## Examples

```bash
# Default (0.0.0.0:8000)
python main.py api

# Custom port
python main.py api --port 8080

# Localhost only
python main.py api --host 127.0.0.1

# Development with auto-reload
python main.py api --reload
```

## Docker

```bash
docker-compose up -d api
```

Access at: http://localhost:8000
