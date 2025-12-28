"""Client chatbot API routes."""

from fastapi import APIRouter, HTTPException, Request

from libs.logger.logger import get_logger
from src.api.schemas.chatbots.client import ClientChatRequest, ClientChatResponse

logger = get_logger(__name__)

router = APIRouter(tags=["client-chatbot"])


@router.post("/chat", response_model=ClientChatResponse)
async def chat(request: Request, body: ClientChatRequest):
    """Client chatbot endpoint.

    For internal business users to query BI data and chat history.

    Args:
        request: FastAPI request object.
        body: Chat request body.

    Returns:
        ClientChatResponse with response, intent, and optional chart_html.
    """
    try:
        service = request.app.state.client_chatbot_service

        result = service.chat(
            query=body.query,
            thread_id=body.thread_id,
            user_id=body.user_id,
        )

        intent = result.get("intent")
        intent_str = intent.value if intent else None

        return ClientChatResponse(
            response=result.get("response", ""),
            thread_id=body.thread_id,
            intent=intent_str,
            chart_html=result.get("chart_html"),
            steps=result.get("steps") if body.include_steps else None,
        )

    except Exception as e:
        logger.error(f"Client chatbot error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
