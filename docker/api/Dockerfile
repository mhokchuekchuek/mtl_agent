FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY libs/ ./libs/
COPY src/ ./src/
COPY configs/ ./configs/

# Expose port
EXPOSE 8000

# Run API via CLI
CMD ["python", "main.py", "api", "--host", "0.0.0.0", "--port", "8000"]
