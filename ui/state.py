"""Application state for ReactPy UI."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Message:
    """A chat message."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    intent: Optional[str] = None
    chart_html: Optional[str] = None


@dataclass
class Session:
    """A chat session."""

    session_id: str
    user_id: str
    name: str
    preview: str = "Start chatting..."
    last_time: Optional[datetime] = None


@dataclass
class AppState:
    """Application state."""

    chatbot_type: str = "customer"  # "customer" or "client"
    sessions: dict = field(default_factory=lambda: {"customer": [], "client": []})
    current_session_id: Optional[str] = None
    current_user_id: Optional[str] = None
    current_session_name: Optional[str] = None
    messages: dict = field(default_factory=dict)  # session_id -> list of Message
    is_loading: bool = False
    show_new_chat_modal: bool = False

    def get_current_sessions(self) -> list:
        """Get sessions for current chatbot type."""
        return self.sessions.get(self.chatbot_type, [])

    def get_current_messages(self) -> list:
        """Get messages for current session."""
        if self.current_session_id:
            return self.messages.get(self.current_session_id, [])
        return []

    def add_session(self, session: dict) -> None:
        """Add a new session."""
        self.sessions[self.chatbot_type].insert(0, session)
        self.messages[session["session_id"]] = []

    def add_message(self, message: dict) -> None:
        """Add a message to current session."""
        if self.current_session_id:
            if self.current_session_id not in self.messages:
                self.messages[self.current_session_id] = []
            self.messages[self.current_session_id].append(message)

    def update_session_preview(self, content: str) -> None:
        """Update preview for current session."""
        for session in self.sessions[self.chatbot_type]:
            if session["session_id"] == self.current_session_id:
                session["preview"] = (
                    content[:30] + "..." if len(content) > 30 else content
                )
                session["last_time"] = datetime.now()
                break

    def copy(self, **kwargs: Any) -> "AppState":
        """Create a copy of state with updated fields."""
        new_state = AppState(
            chatbot_type=kwargs.get("chatbot_type", self.chatbot_type),
            sessions=kwargs.get("sessions", self.sessions.copy()),
            current_session_id=kwargs.get(
                "current_session_id", self.current_session_id
            ),
            current_user_id=kwargs.get("current_user_id", self.current_user_id),
            current_session_name=kwargs.get(
                "current_session_name", self.current_session_name
            ),
            messages=kwargs.get("messages", self.messages.copy()),
            is_loading=kwargs.get("is_loading", self.is_loading),
            show_new_chat_modal=kwargs.get(
                "show_new_chat_modal", self.show_new_chat_modal
            ),
        )
        return new_state
