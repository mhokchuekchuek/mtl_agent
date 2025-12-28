"""Customer chatbot API schemas."""

from typing import Optional

from pydantic import BaseModel


class CustomerChatRequest(BaseModel):
    """Customer chat request schema."""

    query: str
    thread_id: str
    user_id: Optional[str] = None
    include_steps: bool = False


class CustomerChatResponse(BaseModel):
    """Customer chat response schema."""

    response: str
    thread_id: str
    steps: Optional[list[dict]] = None
