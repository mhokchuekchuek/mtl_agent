"""Client chatbot API schemas."""

from typing import Optional

from pydantic import BaseModel


class ClientChatRequest(BaseModel):
    """Client chat request schema."""

    query: str
    thread_id: str
    user_id: Optional[str] = None
    include_steps: bool = False


class ClientChatResponse(BaseModel):
    """Client chat response schema."""

    response: str
    thread_id: str
    intent: Optional[str] = None
    chart_html: Optional[str] = None
    steps: Optional[list[dict]] = None
