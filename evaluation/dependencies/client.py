"""Client chatbot evaluation dependency initialization."""

from evaluation.datasets.loader import DatasetLoader
from evaluation.judges.selector import JudgeSelector
from evaluation.repositories.main import EvaluationRepository
from evaluation.usecases.main import EvaluationService
from libs.configs.selector import ConfigSelector
from libs.database.sql.selector import SQLSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.prompt_manager.selector import PromptManagerSelector


def _format_schema(full_schema: dict) -> str:
    """Format full schema dict as string for LLM."""
    lines = []
    for table_name, columns in full_schema.items():
        lines.append(f"Table: {table_name}")
        for col in columns:
            pk = " (PK)" if col["primary_key"] else ""
            nullable = " NULL" if col["nullable"] else " NOT NULL"
            lines.append(f"  - {col['name']}: {col['type']}{nullable}{pk}")
        lines.append("")
    return "\n".join(lines)


def build_evaluation_service() -> tuple[EvaluationService, str]:
    """Build and return the client evaluation service.

    Returns:
        Tuple of (EvaluationService, dataset_path)
    """
    config = ConfigSelector.create(provider="dynaconf")
    shared = config.shared
    eval_config = config.client_eval

    # === Create shared clients ===

    sql_client = SQLSelector.create(
        provider=shared.database.provider,
        db_path=shared.database.path,
    )
    full_schema = sql_client.get_full_schema()
    schema = _format_schema(full_schema)

    prompt_manager = PromptManagerSelector.create(
        provider=shared.observability.provider,
        host=shared.observability.host,
        public_key=shared.observability.public_key,
        secret_key=shared.observability.secret_key,
    )

    context = getattr(eval_config, "context", "")

    # === Create judges ===

    judges = []

    # SQL Judge
    sql_cfg = getattr(eval_config, "sql_judge", None)
    if sql_cfg and getattr(sql_cfg, "enabled", False):
        prompt_cfg = getattr(sql_cfg, "prompt", None)
        llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=shared.llm.proxy_url,
            api_key=shared.llm.api_key,
            completion_model=getattr(sql_cfg, "model", "gpt-4o"),
            temperature=getattr(sql_cfg, "temperature", 0.0),
            max_tokens=getattr(sql_cfg, "max_tokens", 16384),
        )
        judge = JudgeSelector.create(
            provider="sql",
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            sql_client=sql_client,
            schema=schema,
            prompt_name=prompt_cfg.name if prompt_cfg else "evaluation_sql_judge",
            prompt_label=prompt_cfg.label if prompt_cfg else "latest",
            context=context,
        )
        judges.append(judge)

    # Response Quality Judge
    rq_cfg = getattr(eval_config, "response_quality_judge", None)
    if rq_cfg and getattr(rq_cfg, "enabled", False):
        prompt_cfg = getattr(rq_cfg, "prompt", None)
        llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=shared.llm.proxy_url,
            api_key=shared.llm.api_key,
            completion_model=getattr(rq_cfg, "model", "gpt-4o"),
            temperature=getattr(rq_cfg, "temperature", 0.0),
            max_tokens=getattr(rq_cfg, "max_tokens", 16384),
        )
        judge = JudgeSelector.create(
            provider="response_quality",
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            prompt_name=prompt_cfg.name
            if prompt_cfg
            else "evaluation_response_quality_judge",
            prompt_label=prompt_cfg.label if prompt_cfg else "latest",
            context=context,
        )
        judges.append(judge)

    # Visualization Judge
    viz_cfg = getattr(eval_config, "visualization_judge", None)
    if viz_cfg and getattr(viz_cfg, "enabled", False):
        prompt_cfg = getattr(viz_cfg, "prompt", None)
        llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=shared.llm.proxy_url,
            api_key=shared.llm.api_key,
            completion_model=getattr(viz_cfg, "model", "gpt-4o"),
            temperature=getattr(viz_cfg, "temperature", 0.0),
            max_tokens=getattr(viz_cfg, "max_tokens", 16384),
        )
        judge = JudgeSelector.create(
            provider="visualization",
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            prompt_name=prompt_cfg.name
            if prompt_cfg
            else "evaluation_visualization_judge",
            prompt_label=prompt_cfg.label if prompt_cfg else "latest",
        )
        judges.append(judge)

    # === Create repository ===

    api_config = eval_config.api
    dataset_path = getattr(eval_config, "dataset_path", "evaluation/datasets/client")
    results_path = getattr(eval_config, "results_path", "results/client")
    pass_threshold = getattr(eval_config, "pass_threshold", 0.7)

    evaluation_repo = EvaluationRepository(
        endpoint=api_config.endpoint,
        timeout=getattr(api_config, "timeout", 180),
        judges=judges,
        dataset_loader=DatasetLoader(),
        results_path=results_path,
        pass_threshold=pass_threshold,
        chatbot_name="client",
    )

    # === Create service ===

    service = EvaluationService(evaluation_repo=evaluation_repo)

    return service, dataset_path
