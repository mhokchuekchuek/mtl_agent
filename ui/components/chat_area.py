"""Chat area component with header, messages, and input."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Callable

from reactpy import component, html, use_effect, use_ref, use_state

from ui.api_client import APIError, ClientChatRequest, CustomerChatRequest, ERPApiClient
from ui.components.message_bubble import MessageBubble
from ui.components.typing_indicator import TypingIndicator
from ui.state import AppState
from ui.styles import (
    CHAT_CONTAINER_STYLE,
    CHAT_HEADER_STYLE,
    CHAT_MESSAGES_STYLE,
    CHAT_SUBTITLE_STYLE,
    CHAT_TITLE_STYLE,
    EMPTY_STATE_ICON_STYLE,
    EMPTY_STATE_STYLE,
    EMPTY_STATE_TEXT_STYLE,
    EMPTY_STATE_TITLE_STYLE,
    INPUT_AREA_STYLE,
    INPUT_CONTAINER_STYLE,
    MESSAGE_INPUT_STYLE,
    SEND_BUTTON_STYLE,
    SESSION_INFO_LABEL_STYLE,
    SESSION_INFO_STYLE,
    SESSION_INFO_VALUE_STYLE,
)

logger = logging.getLogger(__name__)

# API client instance
api_client = ERPApiClient()


@component
def ChatHeader(state: AppState):
    """Chat header with title and session info."""
    title = "Customer Support" if state.chatbot_type == "customer" else "BI Analytics"

    return html.div(
        {"style": CHAT_HEADER_STYLE},
        # Left side
        html.div(
            {},
            html.div({"style": CHAT_TITLE_STYLE}, title),
            html.div(
                {"style": CHAT_SUBTITLE_STYLE},
                f"Session: {state.current_session_name or 'Chat'}",
            ),
        ),
        # Right side - session info
        html.div(
            {"style": {"display": "flex", "gap": "8px"}},
            html.div(
                {"style": SESSION_INFO_STYLE},
                html.span({"style": SESSION_INFO_LABEL_STYLE}, "Session ID: "),
                html.span(
                    {"style": SESSION_INFO_VALUE_STYLE}, state.current_session_id
                ),
            ),
            html.div(
                {"style": SESSION_INFO_STYLE},
                html.span({"style": SESSION_INFO_LABEL_STYLE}, "User ID: "),
                html.span({"style": SESSION_INFO_VALUE_STYLE}, state.current_user_id),
            ),
        ),
    )


@component
def MessagesList(state: AppState):
    """List of chat messages."""
    messages = state.get_current_messages()

    # Welcome message if no messages
    if not messages:
        if state.chatbot_type == "customer":
            welcome = "สวัสดีครับ! ยินดีต้อนรับสู่ MTL ERP Assistant 👋\n\nผมช่วยคุณได้เรื่องอะไรบ้างครับ? เช่น:\n• ค้นหาสินค้า\n• ตรวจสอบ stock\n• ดูข้อมูลออเดอร์"
        else:
            welcome = "สวัสดีครับ! ยินดีต้อนรับสู่ BI Analytics 📊\n\nผมช่วยวิเคราะห์ข้อมูลให้คุณได้ เช่น:\n• ยอดขายรายเดือน\n• วิเคราะห์พฤติกรรมลูกค้า\n• สร้างรายงานและแผนภูมิ"

        return html.div(
            {"style": CHAT_MESSAGES_STYLE},
            MessageBubble(
                role="assistant",
                content=welcome,
                timestamp=datetime.now(),
            ),
        )

    # Render all messages
    message_bubbles = [
        MessageBubble(
            role=msg["role"],
            content=msg["content"],
            timestamp=msg.get("timestamp"),
            intent=msg.get("intent"),
            chart_html=msg.get("chart_html"),
        )
        for msg in messages
    ]

    # Add typing indicator if loading
    if state.is_loading:
        message_bubbles.append(TypingIndicator())

    return html.div({"style": CHAT_MESSAGES_STYLE}, *message_bubbles)


def call_api_sync(
    chatbot_type: str,
    session_id: str,
    user_id: str,
    query: str,
) -> dict:
    """Call API synchronously and return response message."""
    logger.info(f"[API] Calling API for {chatbot_type} chat, query: {query[:50]}...")

    try:
        if chatbot_type == "customer":
            request = CustomerChatRequest(
                query=query,
                thread_id=session_id,
                user_id=user_id,
            )
            response = api_client.customer_chat(request)
            logger.info(f"[API] Got customer response: {response.response[:50]}...")
            return {
                "role": "assistant",
                "content": response.response,
                "timestamp": datetime.now(),
            }
        else:
            request = ClientChatRequest(
                query=query,
                thread_id=session_id,
                user_id=user_id,
            )
            response = api_client.client_chat(request)
            logger.info(f"[API] Got client response: {response.response[:50]}...")
            return {
                "role": "assistant",
                "content": response.response,
                "timestamp": datetime.now(),
                "intent": response.intent,
                "chart_html": response.chart_html,
            }
    except APIError as e:
        logger.error(f"[API] APIError: {e}")
        return {
            "role": "assistant",
            "content": f"เกิดข้อผิดพลาด: {str(e)}",
            "timestamp": datetime.now(),
        }
    except Exception as e:
        logger.error(f"[API] Exception: {e}")
        return {
            "role": "assistant",
            "content": f"เกิดข้อผิดพลาด: ไม่สามารถเชื่อมต่อ API ได้ ({str(e)})",
            "timestamp": datetime.now(),
        }


@component
def InputArea(state: AppState, set_state: Callable[[AppState], None]):
    """Message input area."""
    input_value, set_input_value = use_state("")
    # Use a counter to trigger effects - increment to trigger new API call
    request_counter, set_request_counter = use_state(0)
    # Use ref to store pending request data without triggering re-render
    pending_ref = use_ref(None)

    def send_message(event: Any = None):
        """Send user message immediately, then trigger API call."""
        content = input_value.strip()
        logger.info(
            f"[InputArea] send_message called, content: '{content[:30] if content else ''}...'"
        )

        if not content:
            logger.info("[InputArea] Empty content, skipping")
            return
        if not state.current_session_id:
            logger.info("[InputArea] No session_id, skipping")
            return
        if state.is_loading:
            logger.info("[InputArea] Already loading, skipping")
            return

        logger.info(
            f"[InputArea] Processing message for session {state.current_session_id}"
        )

        # Clear input immediately
        set_input_value("")

        # Add user message immediately
        user_msg = {"role": "user", "content": content, "timestamp": datetime.now()}

        new_messages = state.messages.copy()
        if state.current_session_id not in new_messages:
            new_messages[state.current_session_id] = []
        new_messages[state.current_session_id] = new_messages[
            state.current_session_id
        ] + [user_msg]

        # Update state with user message and loading state
        loading_state = state.copy(messages=new_messages, is_loading=True)
        set_state(loading_state)
        logger.info("[InputArea] State updated with user message, is_loading=True")

        # Store request in ref (doesn't trigger re-render)
        # Include the updated messages so we have them when the API responds
        pending_ref.current = {
            "query": content,
            "session_id": state.current_session_id,
            "user_id": state.current_user_id,
            "chatbot_type": state.chatbot_type,
            "messages_snapshot": new_messages,  # Store the messages with user msg included
            "sessions_snapshot": state.sessions.copy(),
        }
        logger.info(f"[InputArea] Set pending_ref with query: {content[:30]}...")

        # Increment counter to trigger effect
        set_request_counter(request_counter + 1)

    def handle_keydown(event: Any):
        if event.get("key") == "Enter" and not event.get("shiftKey"):
            send_message()

    # Use effect to handle API call asynchronously
    @use_effect(dependencies=[request_counter])
    async def fetch_response():
        logger.info(f"[fetch_response] Effect triggered, counter: {request_counter}")

        if not pending_ref.current:
            logger.info("[fetch_response] No pending request in ref, skipping")
            return

        # Extract request info from ref
        request_info = pending_ref.current
        query = request_info["query"]
        session_id = request_info["session_id"]
        user_id = request_info["user_id"]
        chatbot_type = request_info["chatbot_type"]
        messages_snapshot = request_info["messages_snapshot"]
        sessions_snapshot = request_info["sessions_snapshot"]

        # Clear ref immediately
        pending_ref.current = None

        logger.info(f"[fetch_response] Calling API for query: {query[:30]}...")

        # Call API in thread pool to not block
        loop = asyncio.get_event_loop()
        assistant_msg = await loop.run_in_executor(
            None, call_api_sync, chatbot_type, session_id, user_id, query
        )
        logger.info(
            f"[fetch_response] Got response: {assistant_msg['content'][:50]}..."
        )

        # Add assistant message to the snapshot (which already has user message)
        new_messages = messages_snapshot.copy()
        new_messages[session_id] = new_messages.get(session_id, []) + [assistant_msg]

        # Update session preview
        new_sessions = sessions_snapshot.copy()
        for session in new_sessions.get(chatbot_type, []):
            if session["session_id"] == session_id:
                session["preview"] = query[:30] + "..." if len(query) > 30 else query
                session["last_time"] = datetime.now()
                break

        final_state = state.copy(
            messages=new_messages, sessions=new_sessions, is_loading=False
        )
        set_state(final_state)
        logger.info(
            "[fetch_response] State updated with assistant message, is_loading=False"
        )

    return html.div(
        {"style": INPUT_AREA_STYLE},
        html.div(
            {"style": INPUT_CONTAINER_STYLE},
            html.input(
                {
                    "style": MESSAGE_INPUT_STYLE,
                    "type": "text",
                    "placeholder": "พิมพ์ข้อความของคุณ...",
                    "value": input_value,
                    "onChange": lambda e: set_input_value(e["target"]["value"]),
                    "onKeyDown": handle_keydown,
                    "disabled": state.is_loading,
                }
            ),
            html.button(
                {
                    "style": SEND_BUTTON_STYLE,
                    "onClick": send_message,
                    "disabled": state.is_loading,
                },
                "➤",
            ),
        ),
    )


@component
def EmptyState():
    """Empty state when no session is selected."""
    return html.div(
        {"style": EMPTY_STATE_STYLE},
        html.div({"style": EMPTY_STATE_ICON_STYLE}, "💬"),
        html.div({"style": EMPTY_STATE_TITLE_STYLE}, "Select or Create a Session"),
        html.div(
            {"style": EMPTY_STATE_TEXT_STYLE},
            "Choose an existing session from the sidebar or click 'Add New Chat' to start.",
        ),
    )


@component
def ChatArea(state: AppState, set_state: Callable[[AppState], None]):
    """Main chat area with header, messages, and input."""
    if not state.current_session_id:
        return html.main({"style": CHAT_CONTAINER_STYLE}, EmptyState())

    return html.main(
        {"style": CHAT_CONTAINER_STYLE},
        ChatHeader(state),
        MessagesList(state),
        InputArea(state, set_state),
    )
