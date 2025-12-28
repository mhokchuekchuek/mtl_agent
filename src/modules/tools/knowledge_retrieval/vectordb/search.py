"""Product search tool using semantic similarity."""

from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from libs.database.vector.base import BaseVectorStore
from libs.llm.client.base import BaseLLM
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class ProductSearchInput(BaseModel):
    """Input schema for product search tool."""

    query: str = Field(description="Search query text (e.g., 'wireless speaker')")
    top_k: int = Field(default=10, description="Number of results to return")


class ProductSearchTool(BaseTool):
    """Search products using semantic similarity."""

    name: str = "product_search"
    description: str = (
        "Search for products using semantic similarity. "
        "Use this when you need to find products matching a text description."
    )
    args_schema: Type[BaseModel] = ProductSearchInput  # pyright: ignore[reportIncompatibleVariableOverride]
    vector_store: Optional[BaseVectorStore] = None
    llm_client: Optional[BaseLLM] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        vector_store: BaseVectorStore,
        llm_client: BaseLLM,
        **kwargs,
    ):
        """Initialize product search tool.

        Args:
            vector_store: Vector store client.
            llm_client: LLM client for embeddings.
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.vector_store = vector_store
        self.llm_client = llm_client
        logger.info("ProductSearchTool initialized")

    def _run(self, query: str, top_k: int = 10) -> dict:
        """Execute semantic search.

        Args:
            query: Search query text.
            top_k: Number of results to return.

        Returns:
            Dict with query and results.
        """
        logger.info(f"Searching for: {query} (top_k={top_k})")

        try:
            embeddings = self.llm_client.embed([query])
            query_embedding = embeddings[0]

            results = self.vector_store.search(
                query_embedding=query_embedding,
                k=top_k,
            )

            formatted = [
                {
                    "product_id": r["metadata"].get("product_id"),
                    "score": r["score"],
                    "metadata": r["metadata"],
                }
                for r in results
            ]

            logger.info(f"Search returned {len(formatted)} results")
            return {"query": query, "results": formatted}

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {"query": query, "results": [], "error": str(e)}
