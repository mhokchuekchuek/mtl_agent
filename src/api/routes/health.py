"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        dict: Service health status.
    """
    return {"status": "healthy", "service": "erp-agent"}


@router.get("/")
async def root():
    """Root endpoint with API information.

    Returns:
        dict: API information and available endpoints.
    """
    return {
        "service": "ERP Multi-Agent System",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }
