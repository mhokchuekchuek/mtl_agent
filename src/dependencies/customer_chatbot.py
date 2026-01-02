"""Customer chatbot service dependency initialization."""

from libs.configs.selector import ConfigSelector
from libs.database.key_value.selector import KeyValueSelector
from libs.database.sql.selector import SQLSelector
from libs.database.vector.selector import VectorStoreSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.observability.selector import ObservabilitySelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from src.modules.agents.products.main import ProductAgent
from src.modules.agents.translation.main import TranslationAgent
from src.modules.tools.knowledge_retrieval.sql.customer.cancel_order import (
    CancelOrderSQLTool,
)
from src.modules.tools.knowledge_retrieval.sql.customer.order import (
    CustomerOrderSQLTool,
)
from src.modules.tools.knowledge_retrieval.sql.customer.place_order import (
    PlaceOrderSQLTool,
)
from src.modules.tools.knowledge_retrieval.sql.customer.product import (
    CustomerProductSQLTool,
)
from src.modules.tools.knowledge_retrieval.vectordb.search import ProductSearchTool
from src.modules.tools.knowledge_retrieval.vectordb.similar import SimilarProductsTool
from src.modules.workflows.customer_chatbot.main import CustomerChatbotWorkflow
from src.repositories.chatbots.customer.main import CustomerChatbotRepository
from src.repositories.checkpointers.redis.main import RedisCheckpointerRepository
from src.repositories.stores.postgres.main import PostgresStoreRepository
from src.usecases.chatbot.main import ChatbotService


def build_chatbot_service() -> ChatbotService:
    """Build and return the customer chatbot service.

    Creates all dependencies from config and wires them together:
    - Clients: LLM (litellm + langchain), SQL, VectorStore, Observability, PromptManager
    - Repositories: CheckpointerRepository, StoreRepository, ChatbotRepository
    - Tools: SQLTool, ProductSearchTool, SimilarProductsTool
    - Agents: TranslationAgent, ProductAgent
    - Workflow: CustomerChatbotWorkflow
    - Service: ChatbotService

    Returns:
        ChatbotService ready to use.
    """
    # Load config
    config = ConfigSelector.create(provider="dynaconf")
    shared = config.shared
    chatbot = config.customer_chatbot

    prompt_label = chatbot.prompt_label

    # === Create Clients (libs layer) ===

    # LangChain client - for agents (ChatOpenAI)
    langchain_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=shared.llm.default_model,
        default_temperature=shared.llm.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for product SQL tool (generate)
    product_sql_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.products.tools.product_sql.model,
        default_temperature=chatbot.agents.products.tools.product_sql.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for order SQL tool (generate)
    order_sql_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.products.tools.order_sql.model,
        default_temperature=chatbot.agents.products.tools.order_sql.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for place order SQL tool (generate)
    place_order_sql_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.products.tools.place_order_sql.model,
        default_temperature=chatbot.agents.products.tools.place_order_sql.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for cancel order SQL tool (generate)
    cancel_order_sql_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.products.tools.cancel_order_sql.model,
        default_temperature=chatbot.agents.products.tools.cancel_order_sql.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for vector search tools (embed)
    vector_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=shared.llm.default_model,
        default_temperature=shared.llm.temperature,
        default_max_tokens=shared.llm.max_tokens,
        embedding_model=chatbot.agents.products.tools.product_search.embedding_model,
    )

    # SQL client
    sql_client = SQLSelector.create(
        provider=shared.database.provider,
        db_path=shared.database.path,
    )

    # Vector store client
    vector_store = VectorStoreSelector.create(
        provider=shared.vectordb.provider,
        host=shared.vectordb.host,
        port=shared.vectordb.port,
        collection_name=chatbot.vectordb.collection_name,
    )

    # Observability
    observability = ObservabilitySelector.create(
        provider=shared.observability.provider,
        host=shared.observability.host,
        public_key=shared.observability.public_key,
        secret_key=shared.observability.secret_key,
    )

    # Prompt manager
    prompt_manager = PromptManagerSelector.create(
        provider=shared.observability.provider,  # langfuse
        host=shared.observability.host,
        public_key=shared.observability.public_key,
        secret_key=shared.observability.secret_key,
    )

    # === Create Memory Repositories ===

    # Checkpointer repository (short-term memory)
    redis_client = KeyValueSelector.create(
        provider="redis",
        host=shared.checkpointer.host,
        port=int(shared.checkpointer.port),
    )

    checkpoint_repo = RedisCheckpointerRepository(
        redis_client=redis_client,
        ttl=int(shared.checkpointer.ttl),
        refresh_on_read=shared.checkpointer.refresh_on_read,
    )

    # Store repository (long-term memory)
    store_repo = PostgresStoreRepository(
        host=shared.store.host,
        port=int(shared.store.port),
        database=shared.store.database,
        user=shared.store.user,
        password=shared.store.password,
    )

    # === Create Tools ===

    product_sql_tool = CustomerProductSQLTool(
        sql_client=sql_client,
        llm_client=product_sql_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.products.tools.product_sql.prompt_name,
        prompt_label=prompt_label,
        allow_write=chatbot.agents.products.tools.product_sql.allow_write,
        allowed_tables=list(chatbot.agents.products.tools.product_sql.allowed_tables),
    )

    order_sql_tool = CustomerOrderSQLTool(
        sql_client=sql_client,
        llm_client=order_sql_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.products.tools.order_sql.prompt_name,
        prompt_label=prompt_label,
        allow_write=chatbot.agents.products.tools.order_sql.allow_write,
        allowed_tables=list(chatbot.agents.products.tools.order_sql.allowed_tables),
    )

    product_search_tool = ProductSearchTool(
        vector_store=vector_store,
        llm_client=vector_llm_client,
        similarity_threshold=chatbot.agents.products.tools.product_search.similarity_threshold,
    )

    similar_products_tool = SimilarProductsTool(
        vector_store=vector_store,
        llm_client=vector_llm_client,
    )

    place_order_sql_tool = PlaceOrderSQLTool(
        sql_client=sql_client,
        llm_client=place_order_sql_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.products.tools.place_order_sql.prompt_name,
        prompt_label=prompt_label,
        allow_write=chatbot.agents.products.tools.place_order_sql.allow_write,
        allowed_tables=list(
            chatbot.agents.products.tools.place_order_sql.allowed_tables
        ),
    )

    cancel_order_sql_tool = CancelOrderSQLTool(
        sql_client=sql_client,
        llm_client=cancel_order_sql_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.products.tools.cancel_order_sql.prompt_name,
        prompt_label=prompt_label,
        allow_write=chatbot.agents.products.tools.cancel_order_sql.allow_write,
        allowed_tables=list(
            chatbot.agents.products.tools.cancel_order_sql.allowed_tables
        ),
    )

    # === Create Agents ===

    # Translation agent - uses langchain (generate)
    translation_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.translation.model,
        default_temperature=chatbot.agents.translation.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    translation_agent = TranslationAgent(
        llm_client=translation_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.translation.prompt_name,
        prompt_label=prompt_label,
    )

    # Product agent - uses langchain (ChatOpenAI for ReAct)
    product_llm = langchain_client.get_client(
        model=chatbot.agents.products.model,
        temperature=chatbot.agents.products.temperature,
    )

    product_agent = ProductAgent(
        llm=product_llm,
        prompt_manager=prompt_manager,
        tools=[
            product_sql_tool,
            order_sql_tool,
            place_order_sql_tool,
            cancel_order_sql_tool,
            product_search_tool,
            similar_products_tool,
        ],
        prompt_name=chatbot.agents.products.prompt_name,
        prompt_label=prompt_label,
        max_iterations=chatbot.agents.products.max_iterations,
    )

    # === Create Workflow (uncompiled) ===

    workflow = CustomerChatbotWorkflow(
        translation_agent=translation_agent,
        product_agent=product_agent,
    )

    # === Create Chatbot Repository (compiles workflow + memory) ===

    chatbot_repo = CustomerChatbotRepository(
        workflow=workflow,
        checkpoint_repo=checkpoint_repo,
        store_repo=store_repo,
        observability=observability,
    )

    # === Create Service ===

    return ChatbotService(chatbot_repo=chatbot_repo)
