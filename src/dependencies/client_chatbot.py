"""Client chatbot service dependency initialization."""

from libs.configs.selector import ConfigSelector
from libs.database.key_value.selector import KeyValueSelector
from libs.database.sql.postgres.main import PostgreSQLClient
from libs.database.sql.selector import SQLSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.observability.selector import ObservabilitySelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from src.modules.agents.client.chat_history import CustomerChatHistoryAgent
from src.modules.agents.client.insight import CustomerInsightAgent
from src.modules.agents.client.orchestrator import OrchestratorAgent
from src.modules.agents.translation.main import TranslationAgent
from src.modules.tools.knowledge_retrieval.sql.main import SQLTool
from src.modules.tools.visualization.main import VisualizationTool
from src.modules.workflows.client_chatbot.main import ClientChatbotWorkflow
from src.repositories.chatbots.client.main import ClientChatbotRepository
from src.repositories.checkpointers.redis.main import RedisCheckpointerRepository
from src.usecases.chatbot.main import ChatbotService


def build_client_chatbot_service() -> ChatbotService:
    """Build and return the client chatbot service.

    Creates all dependencies from config and wires them together:
    - Clients: LLM (litellm + langchain), SQL (PostgreSQL + SQLite), Observability, PromptManager
    - Repositories: CheckpointerRepository, StoreRepository, ClientChatbotRepository
    - Tools: SQLTool (PostgreSQL), SQLTool (SQLite), VisualizationTool
    - Agents: TranslationAgent, OrchestratorAgent, CustomerChatHistoryAgent, CustomerInsightAgent
    - Workflow: ClientChatbotWorkflow
    - Service: ChatbotService

    Returns:
        ChatbotService ready to use.
    """
    # Load config
    config = ConfigSelector.create(provider="dynaconf")
    shared = config.shared
    chatbot = config.client_chatbot

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

    # LangChain client - for chat history SQL tool
    chat_history_sql_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.chat_history.tools.sql.model,
        default_temperature=chatbot.agents.chat_history.tools.sql.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for insight SQL tool
    insight_sql_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.insight.tools.sql.model,
        default_temperature=chatbot.agents.insight.tools.sql.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # LangChain client - for visualization tool
    viz_llm_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=shared.llm.proxy_url,
        api_key=shared.llm.api_key,
        default_model=chatbot.agents.insight.tools.visualization.model,
        default_temperature=chatbot.agents.insight.tools.visualization.temperature,
        default_max_tokens=shared.llm.max_tokens,
    )

    # SQL client - PostgreSQL for chat history
    postgres_client = PostgreSQLClient(
        host=shared.store.host,
        port=int(shared.store.port),
        database=shared.store.database,
        user=shared.store.user,
        password=shared.store.password,
    )

    # SQL client - SQLite for ERP data
    sqlite_client = SQLSelector.create(
        provider=shared.database.provider,
        db_path=shared.database.path,
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

    # No store for client_chatbot (internal BI tool, no long-term memory needed)

    # === Create Tools ===

    # SQL tool for PostgreSQL (chat history)
    sql_tool_postgres = SQLTool(
        sql_client=postgres_client,
        llm_client=chat_history_sql_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.chat_history.tools.sql.prompt_name,
        prompt_label=prompt_label,
        allow_write=False,
    )

    # SQL tool for SQLite (ERP data)
    sql_tool_sqlite = SQLTool(
        sql_client=sqlite_client,
        llm_client=insight_sql_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.insight.tools.sql.prompt_name,
        prompt_label=prompt_label,
        allow_write=False,
    )

    # Visualization tool
    visualization_tool = VisualizationTool(
        llm_client=viz_llm_client,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.insight.tools.visualization.prompt_name,
        prompt_label=prompt_label,
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

    # Orchestrator agent - uses langchain
    orchestrator_llm = langchain_client.get_client(
        model=chatbot.agents.orchestrator.model,
        temperature=chatbot.agents.orchestrator.temperature,
    )

    orchestrator_agent = OrchestratorAgent(
        llm=orchestrator_llm,
        prompt_manager=prompt_manager,
        prompt_name=chatbot.agents.orchestrator.prompt_name,
        prompt_label=prompt_label,
    )

    # Chat history agent - uses langchain (ReAct)
    chat_history_llm = langchain_client.get_client(
        model=chatbot.agents.chat_history.model,
        temperature=chatbot.agents.chat_history.temperature,
    )

    chat_history_agent = CustomerChatHistoryAgent(
        llm=chat_history_llm,
        prompt_manager=prompt_manager,
        tools=[sql_tool_postgres],
        prompt_name=chatbot.agents.chat_history.prompt_name,
        prompt_label=prompt_label,
        max_iterations=chatbot.agents.chat_history.max_iterations,
        recursion_limit=chatbot.agents.chat_history.recursion_limit,
    )

    # Insight agent - uses langchain (ReAct)
    insight_llm = langchain_client.get_client(
        model=chatbot.agents.insight.model,
        temperature=chatbot.agents.insight.temperature,
    )

    insight_agent = CustomerInsightAgent(
        llm=insight_llm,
        prompt_manager=prompt_manager,
        tools=[sql_tool_sqlite, visualization_tool],
        prompt_name=chatbot.agents.insight.prompt_name,
        prompt_label=prompt_label,
        max_iterations=chatbot.agents.insight.max_iterations,
        recursion_limit=chatbot.agents.insight.recursion_limit,
    )

    # === Create Workflow (uncompiled) ===

    workflow = ClientChatbotWorkflow(
        translation_agent=translation_agent,
        orchestrator_agent=orchestrator_agent,
        chat_history_agent=chat_history_agent,
        insight_agent=insight_agent,
    )

    # === Create Chatbot Repository (compiles workflow + memory) ===

    chatbot_repo = ClientChatbotRepository(
        workflow=workflow,
        checkpoint_repo=checkpoint_repo,
        store_repo=None,  # No long-term memory for client_chatbot
        observability=observability,
    )

    # === Create Service ===

    return ChatbotService(chatbot_repo=chatbot_repo)
