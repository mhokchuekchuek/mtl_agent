"""UI configuration settings."""

import os


class UIConfig:
    """Configuration for UI."""

    # API endpoints
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    CUSTOMER_CHAT_ENDPOINT: str = "/api/v1/chatbot/customer/chat"
    CLIENT_CHAT_ENDPOINT: str = "/api/v1/chatbot/client/chat"
    HEALTH_ENDPOINT: str = "/health"

    # Request settings
    REQUEST_TIMEOUT: int = 120  # seconds
