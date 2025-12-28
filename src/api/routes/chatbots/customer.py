"""Customer chatbot API routes."""

from fastapi import APIRouter, HTTPException, Request

from libs.logger.logger import get_logger
from src.api.schemas.chatbots.customer import CustomerChatRequest, CustomerChatResponse

logger = get_logger(__name__)

router = APIRouter(tags=["customer-chatbot"])


@router.post("/chat", response_model=CustomerChatResponse)
async def chat(request: Request, body: CustomerChatRequest):
    """Customer chatbot endpoint.

    For customers to ask about products, orders, etc.

    Args:
        request: FastAPI request object.
        body: Chat request body.

    Returns:
        CustomerChatResponse with response text.
    """
    try:
        service = request.app.state.customer_chatbot_service

        result = service.chat(
            query=body.query,
            thread_id=body.thread_id,
            user_id=body.user_id,
        )

        return CustomerChatResponse(
            response=result.get("response", ""),
            thread_id=body.thread_id,
            steps=result.get("steps") if body.include_steps else None,
        )

    except Exception as e:
        logger.error(f"Customer chatbot error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
