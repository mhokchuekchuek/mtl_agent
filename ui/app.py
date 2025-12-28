"""MTL ERP Assistant - ReactPy UI (matching mockup design)."""

from reactpy import component, html, use_state

from ui.components.chat_area import ChatArea
from ui.components.header import Header
from ui.components.new_chat_modal import NewChatModal
from ui.components.sidebar import Sidebar
from ui.state import AppState
from ui.styles import APP_CONTAINER_STYLE, GLOBAL_STYLES, MAIN_CONTAINER_STYLE


@component
def App():
    """Main application component."""
    state, set_state = use_state(AppState())

    return html.div(
        {"style": APP_CONTAINER_STYLE},
        # Inject global styles
        html.style(GLOBAL_STYLES),
        # Header
        Header(),
        # Main container with sidebar and chat area
        html.div(
            {"style": MAIN_CONTAINER_STYLE},
            Sidebar(state, set_state),
            ChatArea(state, set_state),
        ),
        # Modal (conditionally rendered)
        NewChatModal(state, set_state),
    )


def run_ui(host: str = "0.0.0.0", port: int = 8501):
    """Run the ReactPy app with FastAPI backend."""
    import uvicorn

    from ui.server import app as fastapi_app

    uvicorn.run(fastapi_app, host=host, port=port)


if __name__ == "__main__":
    run_ui()
