"""Sidebar component with chatbot tabs, sessions list, and new chat button."""

from typing import Any, Callable

from reactpy import component, html

from ui.state import AppState
from ui.styles import (
    CHATBOT_TAB_ACTIVE_STYLE,
    CHATBOT_TAB_STYLE,
    CHATBOT_TABS_STYLE,
    NEW_CHAT_BTN_STYLE,
    NEW_CHAT_SECTION_STYLE,
    SESSION_BADGE_STYLE,
    SESSION_ITEM_ACTIVE_STYLE,
    SESSION_ITEM_STYLE,
    SESSION_META_STYLE,
    SESSION_PREVIEW_STYLE,
    SESSION_TITLE_STYLE,
    SESSIONS_CONTAINER_STYLE,
    SESSIONS_HEADER_STYLE,
    SIDEBAR_STYLE,
    TEXT_LIGHTER,
)


@component
def ChatbotTabs(state: AppState, set_state: Callable[[AppState], None]):
    """Tabs for switching between Customer and Client chatbots."""

    def switch_to_customer(event: Any):
        new_state = state.copy(
            chatbot_type="customer",
            current_session_id=None,
            current_user_id=None,
            current_session_name=None,
        )
        set_state(new_state)

    def switch_to_client(event: Any):
        new_state = state.copy(
            chatbot_type="client",
            current_session_id=None,
            current_user_id=None,
            current_session_name=None,
        )
        set_state(new_state)

    customer_style = (
        CHATBOT_TAB_ACTIVE_STYLE
        if state.chatbot_type == "customer"
        else CHATBOT_TAB_STYLE
    )
    client_style = (
        CHATBOT_TAB_ACTIVE_STYLE
        if state.chatbot_type == "client"
        else CHATBOT_TAB_STYLE
    )

    return html.div(
        {"style": CHATBOT_TABS_STYLE},
        html.button(
            {"style": customer_style, "onClick": switch_to_customer},
            html.span({"style": {"fontSize": "20px"}}, "💬"),
            html.span({}, "Customer"),
        ),
        html.button(
            {"style": client_style, "onClick": switch_to_client},
            html.span({"style": {"fontSize": "20px"}}, "📊"),
            html.span({}, "Client"),
        ),
    )


@component
def SessionItem(
    session: dict,
    is_active: bool,
    on_select: Callable[[], None],
):
    """Individual session item."""
    style = SESSION_ITEM_ACTIVE_STYLE if is_active else SESSION_ITEM_STYLE

    # Format time
    time_str = ""
    if session.get("last_time"):
        time_str = session["last_time"].strftime("%H:%M")

    return html.div(
        {"style": style, "onClick": lambda e: on_select()},
        # Title row
        html.div(
            {"style": SESSION_TITLE_STYLE},
            html.span({}, session.get("name", "Chat")),
            html.span({"style": SESSION_BADGE_STYLE}, "Active") if is_active else None,
        ),
        # Preview
        html.div(
            {"style": SESSION_PREVIEW_STYLE},
            session.get("preview", "Start chatting...")[:40],
        ),
        # Meta row
        html.div(
            {"style": SESSION_META_STYLE},
            html.span({}, session.get("user_id", "")),
            html.span({}, time_str),
        ),
    )


@component
def SessionsList(state: AppState, set_state: Callable[[AppState], None]):
    """List of sessions for current chatbot type."""
    sessions = state.get_current_sessions()

    def select_session(session: dict):
        new_state = state.copy(
            current_session_id=session["session_id"],
            current_user_id=session["user_id"],
            current_session_name=session.get("name", "Chat"),
        )
        set_state(new_state)

    if not sessions:
        return html.div(
            {"style": SESSIONS_CONTAINER_STYLE},
            html.div({"style": SESSIONS_HEADER_STYLE}, "Recent Sessions"),
            html.div(
                {
                    "style": {
                        "padding": "32px",
                        "textAlign": "center",
                        "color": TEXT_LIGHTER,
                    }
                },
                html.div({"style": {"fontSize": "14px"}}, "No sessions yet."),
                html.div(
                    {"style": {"fontSize": "12px", "marginTop": "4px"}},
                    "Click 'Add New Chat' to start.",
                ),
            ),
        )

    session_items = [
        SessionItem(
            session=session,
            is_active=session["session_id"] == state.current_session_id,
            on_select=lambda s=session: select_session(s),
        )
        for session in sessions
    ]

    return html.div(
        {"style": SESSIONS_CONTAINER_STYLE},
        html.div({"style": SESSIONS_HEADER_STYLE}, "Recent Sessions"),
        *session_items,
    )


@component
def NewChatButton(state: AppState, set_state: Callable[[AppState], None]):
    """Button to open new chat modal."""

    def open_modal(event: Any):
        new_state = state.copy(show_new_chat_modal=True)
        set_state(new_state)

    return html.div(
        {"style": NEW_CHAT_SECTION_STYLE},
        html.button(
            {"style": NEW_CHAT_BTN_STYLE, "onClick": open_modal},
            html.span({}, "+"),
            html.span({}, "Add New Chat"),
        ),
    )


@component
def Sidebar(state: AppState, set_state: Callable[[AppState], None]):
    """Sidebar with chatbot tabs, sessions list, and new chat button."""
    return html.aside(
        {"style": SIDEBAR_STYLE},
        ChatbotTabs(state, set_state),
        SessionsList(state, set_state),
        NewChatButton(state, set_state),
    )
