"""Customer chatbot repository."""

from typing import Optional

from libs.llm.observability.base import BaseObservability
from libs.logger.logger import get_logger
from src.modules.workflows.customer_chatbot.main import CustomerChatbotWorkflow
from src.repositories.chatbots.base import BaseChatbotRepository
from src.repositories.checkpointers.base import BaseCheckpointerRepository
from src.repositories.stores.base import BaseStoreRepository

logger = get_logger(__name__)


class CustomerChatbotRepository(BaseChatbotRepository):
    """Repository for customer chatbot.

    Compiles workflow with checkpointer and store.
    Manages memory and conversation history.
    """

    def __init__(
        self,
        workflow: CustomerChatbotWorkflow,
        checkpoint_repo: Optional[BaseCheckpointerRepository] = None,
        store_repo: Optional[BaseStoreRepository] = None,
        observability: Optional[BaseObservability] = None,
    ):
        """Initialize customer chatbot repository.

        Args:
            workflow: Workflow definition (uncompiled).
            checkpoint_repo: Repository for short-term memory.
            store_repo: Repository for long-term memory.
            observability: Optional observability for tracing.
        """
        super().__init__(checkpoint_repo, store_repo)
        self.observability = observability

        # Compile graph with memory
        checkpointer = checkpoint_repo.checkpointer if checkpoint_repo else None
        store = store_repo.store if store_repo else None
        self.app = workflow.build().compile(checkpointer=checkpointer, store=store)

    def invoke(
        self,
        query: str,
        thread_id: str,
        user_id: Optional[str] = None,
    ) -> dict:
        """Invoke the chatbot.

        Args:
            query: User's query.
            thread_id: Thread ID for conversation memory.
            user_id: Optional user ID for observability and store.

        Returns:
            Final state with response and steps.
        """
        # Get conversation history from checkpointer
        history = self.get_history(thread_id)
        logger.info(
            f"Retrieved {len(history)} messages from history for thread {thread_id}"
        )

        initial_state = {
            "messages": history,
            "query": query,
            "customer_id": user_id,
            "user_language": None,
            "translated_query": None,
            "response": None,
            "error": None,
            "steps": [],
        }

        run_config = {"configurable": {"thread_id": thread_id}}

        if self.observability:
            callback_handler = self.observability.get_callback_handler(
                session_id=thread_id,
                user_id=user_id,
            )
            if callback_handler:
                run_config["callbacks"] = [callback_handler]

        result = self.app.invoke(initial_state, config=run_config)

        # Save to long-term memory
        self._save_to_store(
            query=query,
            response=result.get("response"),
            thread_id=thread_id,
            user_id=user_id,
        )

        if self.observability:
            self.observability.flush()

        return result
