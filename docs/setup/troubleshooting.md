# Troubleshooting

Common issues and solutions.

## Docker Issues

### View Logs

```bash
docker-compose logs -f
docker-compose logs -f <service_name>
```

### Restart Services

```bash
docker-compose restart
```

### Clean Restart

```bash
docker-compose down -v
docker-compose up -d
```

## Python Issues

### Check Version

```bash
python --version  # Should be 3.10+
```

### Reinstall Dependencies

```bash
pip install -r requirements.txt --force-reinstall
```

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Connection Issues

### Check Services Running

```bash
docker-compose ps
```

### Check Ports

```bash
# Qdrant
curl http://localhost:6333/health

# LiteLLM
curl http://localhost:4000/health

# API
curl http://localhost:8000/health
```
