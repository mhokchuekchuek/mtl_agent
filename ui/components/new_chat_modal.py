"""New chat modal component."""

import uuid
from datetime import datetime
from typing import Any, Callable

from reactpy import component, html, use_state

from ui.state import AppState
from ui.styles import (
    BTN_PRIMARY_STYLE,
    BTN_SECONDARY_STYLE,
    FORM_GROUP_STYLE,
    FORM_HINT_STYLE,
    FORM_INPUT_STYLE,
    FORM_LABEL_STYLE,
    MODAL_ACTIONS_STYLE,
    MODAL_CLOSE_STYLE,
    MODAL_HEADER_STYLE,
    MODAL_OVERLAY_STYLE,
    MODAL_STYLE,
)


@component
def NewChatModal(state: AppState, set_state: Callable[[AppState], None]):
    """Modal for creating a new chat session."""
    # Local form state
    session_id, set_session_id = use_state(f"sess_{uuid.uuid4().hex[:8]}")
    user_id, set_user_id = use_state("")
    session_name, set_session_name = use_state("")

    def close_modal(event: Any = None):
        # Reset form and close
        set_session_id(f"sess_{uuid.uuid4().hex[:8]}")
        set_user_id("")
        set_session_name("")
        new_state = state.copy(show_new_chat_modal=False)
        set_state(new_state)

    def handle_overlay_click(event: Any):
        # Only close if clicking directly on overlay (not on modal content)
        # Check if the click target is the overlay itself
        target = event.get("target", {})
        current_target = event.get("currentTarget", {})
        # If target equals currentTarget, user clicked on overlay background
        if target == current_target:
            close_modal()

    def create_chat(event: Any):
        if not session_id.strip() or not user_id.strip():
            return

        # Create new session
        new_session = {
            "session_id": session_id.strip(),
            "user_id": user_id.strip(),
            "name": session_name.strip() or "New Chat",
            "preview": "Start chatting...",
            "last_time": datetime.now(),
        }

        # Update state with new session and select it
        new_sessions = state.sessions.copy()
        if state.chatbot_type not in new_sessions:
            new_sessions[state.chatbot_type] = []
        new_sessions[state.chatbot_type] = [new_session] + new_sessions[
            state.chatbot_type
        ]

        new_messages = state.messages.copy()
        new_messages[session_id.strip()] = []

        new_state = state.copy(
            sessions=new_sessions,
            messages=new_messages,
            current_session_id=session_id.strip(),
            current_user_id=user_id.strip(),
            current_session_name=session_name.strip() or "New Chat",
            show_new_chat_modal=False,
        )
        set_state(new_state)

        # Reset form
        set_session_id(f"sess_{uuid.uuid4().hex[:8]}")
        set_user_id("")
        set_session_name("")

    if not state.show_new_chat_modal:
        return None

    return html.div(
        {
            "style": MODAL_OVERLAY_STYLE,
            "className": "modal-overlay",
            "onClick": handle_overlay_click,
        },
        html.div(
            {"style": MODAL_STYLE},
            # Header
            html.div(
                {"style": MODAL_HEADER_STYLE},
                html.span({}, "Create New Chat Session"),
                html.button(
                    {"style": MODAL_CLOSE_STYLE, "onClick": close_modal},
                    "×",
                ),
            ),
            # Form
            html.div(
                {"style": FORM_GROUP_STYLE},
                html.label({"style": FORM_LABEL_STYLE}, "Session ID *"),
                html.input(
                    {
                        "style": FORM_INPUT_STYLE,
                        "type": "text",
                        "value": session_id,
                        "placeholder": "e.g., sess_xyz789",
                        "onChange": lambda e: set_session_id(e["target"]["value"]),
                    }
                ),
                html.div(
                    {"style": FORM_HINT_STYLE},
                    "Unique identifier for this conversation",
                ),
            ),
            html.div(
                {"style": FORM_GROUP_STYLE},
                html.label({"style": FORM_LABEL_STYLE}, "User ID *"),
                html.input(
                    {
                        "style": FORM_INPUT_STYLE,
                        "type": "text",
                        "value": user_id,
                        "placeholder": "e.g., user_001",
                        "onChange": lambda e: set_user_id(e["target"]["value"]),
                    }
                ),
                html.div(
                    {"style": FORM_HINT_STYLE},
                    "Your user identifier for tracking",
                ),
            ),
            html.div(
                {"style": FORM_GROUP_STYLE},
                html.label({"style": FORM_LABEL_STYLE}, "Session Name (optional)"),
                html.input(
                    {
                        "style": FORM_INPUT_STYLE,
                        "type": "text",
                        "value": session_name,
                        "placeholder": "e.g., สอบถามราคาสินค้า",
                        "onChange": lambda e: set_session_name(e["target"]["value"]),
                    }
                ),
                html.div(
                    {"style": FORM_HINT_STYLE},
                    "A friendly name for this session",
                ),
            ),
            # Actions
            html.div(
                {"style": MODAL_ACTIONS_STYLE},
                html.button(
                    {"style": BTN_SECONDARY_STYLE, "onClick": close_modal},
                    "Cancel",
                ),
                html.button(
                    {"style": BTN_PRIMARY_STYLE, "onClick": create_chat},
                    "Create Chat",
                ),
            ),
        ),
    )
