"""HTTP client for FastAPI chatbot endpoints."""

from dataclasses import dataclass
from typing import Optional

import requests
from requests.exceptions import ConnectionError, Timeout

from ui.config import UIConfig


@dataclass
class CustomerChatRequest:
    """Customer chat request schema."""

    query: str
    thread_id: str
    user_id: Optional[str] = None

    def to_dict(self) -> dict:
        data = {"query": self.query, "thread_id": self.thread_id}
        if self.user_id:
            data["user_id"] = self.user_id
        return data


@dataclass
class CustomerChatResponse:
    """Customer chat response schema."""

    response: str
    thread_id: str


@dataclass
class ClientChatRequest:
    """Client chat request schema."""

    query: str
    thread_id: str
    user_id: Optional[str] = None

    def to_dict(self) -> dict:
        data = {"query": self.query, "thread_id": self.thread_id}
        if self.user_id:
            data["user_id"] = self.user_id
        return data


@dataclass
class ClientChatResponse:
    """Client chat response schema."""

    response: str
    thread_id: str
    intent: Optional[str] = None
    chart_html: Optional[str] = None


class APIError(Exception):
    """API request error."""

    pass


class ERPApiClient:
    """HTTP client for ERP chatbot API endpoints."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        config = UIConfig()
        self.base_url = (base_url or config.API_BASE_URL).rstrip("/")
        self.timeout = timeout or config.REQUEST_TIMEOUT
        self.config = config

    def health_check(self) -> bool:
        """Check if API server is available."""
        try:
            response = requests.get(
                f"{self.base_url}{self.config.HEALTH_ENDPOINT}",
                timeout=5,
            )
            return response.status_code == 200
        except (ConnectionError, Timeout):
            return False

    def customer_chat(self, request: CustomerChatRequest) -> CustomerChatResponse:
        """Send message to customer chatbot."""
        try:
            response = requests.post(
                f"{self.base_url}{self.config.CUSTOMER_CHAT_ENDPOINT}",
                json=request.to_dict(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return CustomerChatResponse(
                response=data["response"],
                thread_id=data["thread_id"],
            )
        except ConnectionError:
            raise APIError("Cannot connect to API server. Is it running?")
        except Timeout:
            raise APIError("Request timed out. Please try again.")
        except requests.HTTPError as e:
            raise APIError(f"API error: {e.response.text}")

    def client_chat(self, request: ClientChatRequest) -> ClientChatResponse:
        """Send message to client/BI chatbot."""
        try:
            response = requests.post(
                f"{self.base_url}{self.config.CLIENT_CHAT_ENDPOINT}",
                json=request.to_dict(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return ClientChatResponse(
                response=data["response"],
                thread_id=data["thread_id"],
                intent=data.get("intent"),
                chart_html=data.get("chart_html"),
            )
        except ConnectionError:
            raise APIError("Cannot connect to API server. Is it running?")
        except Timeout:
            raise APIError("Request timed out. Please try again.")
        except requests.HTTPError as e:
            raise APIError(f"API error: {e.response.text}")
