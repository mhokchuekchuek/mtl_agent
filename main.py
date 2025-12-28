"""Application CLI entry point.

Usage:
    python main.py api          # Start FastAPI server
    python main.py ui           # Start Streamlit UI
    python main.py api --port 8080
    python main.py ui --port 8502
"""

import subprocess
import sys

import typer
import uvicorn
from dotenv import load_dotenv

from libs.configs.selector import ConfigSelector
from libs.logger.logger import get_logger, setup_logging
from src.api.app import create_app

load_dotenv()

settings = ConfigSelector.create(provider="dynaconf")
setup_logging(level=settings.get("LOG_LEVEL", "INFO"))

logger = get_logger(__name__)

app = typer.Typer(
    name="mtl-agent",
    help="ERP Multi-Agent System CLI",
    add_completion=False,
)


@app.command()
def api(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """Start FastAPI REST API server."""
    logger.info(f"Starting API server on {host}:{port}")
    fastapi_app = create_app(settings=settings)
    uvicorn.run(
        fastapi_app,
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def customer_ui(
    port: int = typer.Option(8501, "--port", "-p", help="Port to bind"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind"),
):
    """Start Customer Support Streamlit UI."""
    logger.info(f"Starting Customer UI on {host}:{port}")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "ui/customer_app.py",
            "--server.address",
            host,
            "--server.port",
            str(port),
            "--server.headless",
            "true",
        ]
    )


@app.command()
def client_ui(
    port: int = typer.Option(8502, "--port", "-p", help="Port to bind"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind"),
):
    """Start Client BI Analytics Streamlit UI."""
    logger.info(f"Starting Client UI on {host}:{port}")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "ui/client_app.py",
            "--server.address",
            host,
            "--server.port",
            str(port),
            "--server.headless",
            "true",
        ]
    )


if __name__ == "__main__":
    app()
