"""Similar products tool using vector similarity."""

from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from libs.database.vector.base import BaseVectorStore
from libs.llm.client.base import BaseLLM
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class SimilarProductsInput(BaseModel):
    """Input schema for similar products tool."""

    product_id: int = Field(description="Base product ID to find similar products for")
    top_k: int = Field(default=5, description="Number of similar products to return")


class SimilarProductsTool(BaseTool):
    """Find products similar to a given product."""

    name: str = "similar_products"
    description: str = (
        "Find products similar to a given product. "
        "Use this when you need to recommend alternatives or related products."
    )
    args_schema: Type[BaseModel] = SimilarProductsInput
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
        """Initialize similar products tool.

        Args:
            vector_store: Vector store client.
            llm_client: LLM client (for consistency).
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.vector_store = vector_store
        self.llm_client = llm_client
        logger.info("SimilarProductsTool initialized")

    def _run(self, product_id: int, top_k: int = 5) -> dict:
        """Find similar products.

        Args:
            product_id: Base product ID.
            top_k: Number of similar products to return.

        Returns:
            Dict with product_id and results.
        """
        logger.info(f"Finding similar products for product_id={product_id}")

        try:
            records = self.vector_store.get(
                filter={"product_id": product_id},
                with_vectors=True,
                limit=1,
            )

            if not records:
                logger.warning(f"Product {product_id} not found in vector store")
                return {"product_id": product_id, "results": []}

            product_embedding = records[0]["vector"]

            results = self.vector_store.search(
                query_embedding=product_embedding,
                k=top_k + 1,
            )

            similar = [
                {
                    "product_id": r["metadata"].get("product_id"),
                    "score": r["score"],
                    "metadata": r["metadata"],
                }
                for r in results
                if r["metadata"].get("product_id") != product_id
            ][:top_k]

            logger.info(f"Found {len(similar)} similar products")
            return {"product_id": product_id, "results": similar}

        except Exception as e:
            logger.error(f"Similar products search failed: {e}")
            return {"product_id": product_id, "results": [], "error": str(e)}
