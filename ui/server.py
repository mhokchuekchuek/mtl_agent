"""FastAPI server with ReactPy integration."""

import logging

from fastapi import FastAPI
from reactpy.backend.fastapi import configure

from ui.app import App

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="MTL ERP Assistant")

# Configure ReactPy with FastAPI
configure(app, App)


def run_ui_server(host: str = "0.0.0.0", port: int = 8501):
    """Run the UI server."""
    import uvicorn

    logger.info(f"Starting UI server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_ui_server()
