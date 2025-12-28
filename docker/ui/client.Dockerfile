FROM python:3.11-slim

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
COPY ui/ ./ui/
COPY configs/ ./configs/

# Expose Streamlit port
EXPOSE 8502

# Run Client BI Streamlit UI
CMD ["python", "main.py", "client-ui", "--host", "0.0.0.0", "--port", "8502"]
