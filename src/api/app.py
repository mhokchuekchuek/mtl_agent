"""FastAPI application factory."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from libs.configs.base import BaseConfigManager
from libs.logger.logger import get_logger
from src.api.routes import health
from src.api.routes.chatbots import client as client_chatbot
from src.api.routes.chatbots import customer as customer_chatbot
from src.dependencies.client_chatbot import build_client_chatbot_service
from src.dependencies.customer_chatbot import build_chatbot_service

logger = get_logger(__name__)


def create_app(settings: BaseConfigManager) -> FastAPI:
    """Create and configure FastAPI application.

    Args:
        settings: Application settings (injected from main.py).

    Returns:
        Configured FastAPI application instance.
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Application lifespan manager."""
        logger.info("Starting up application...")
        # Store settings in app state for access in routes
        app.state.settings = settings

        # Initialize chatbot services
        logger.info("Initializing customer chatbot service...")
        app.state.customer_chatbot_service = build_chatbot_service()

        logger.info("Initializing client chatbot service...")
        app.state.client_chatbot_service = build_client_chatbot_service()

        logger.info("Application startup complete")
        yield
        logger.info("Shutting down application...")

    app = FastAPI(
        title="ERP Multi-Agent System",
        description="AI-powered ERP assistant using LiteLLM, LangGraph, and Qdrant",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router)
    app.include_router(customer_chatbot.router, prefix="/api/v1/chatbot/customer")
    app.include_router(client_chatbot.router, prefix="/api/v1/chatbot/client")

    return app
