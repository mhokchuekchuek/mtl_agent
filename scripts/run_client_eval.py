#!/usr/bin/env python3
"""Run evaluation for Client BI Analytics Chatbot."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests

from evaluation.datasets.loader import DatasetLoader
from evaluation.judges.response_quality_judge import ResponseQualityJudge
from evaluation.judges.sql_judge import SQLJudge
from evaluation.judges.visualization_judge import VisualizationJudge
from evaluation.runner import EvaluationConfig, EvaluationRunner
from libs.configs.selector import ConfigSelector
from libs.database.sql.selector import SQLSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from libs.logger.logger import get_logger, setup_logging

settings = ConfigSelector.create(provider="dynaconf")
setup_logging(level=settings.get("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

eval_config = settings.client_eval


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


def create_judges():
    """Create judges based on config."""
    shared = settings.shared

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

    judges = []
    context = getattr(eval_config, "context", "")

    # SQL Judge
    sql_judge_cfg = getattr(eval_config, "sql_judge", None)
    if sql_judge_cfg and getattr(sql_judge_cfg, "enabled", False):
        llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=shared.llm.proxy_url,
            api_key=shared.llm.api_key,
            completion_model=getattr(sql_judge_cfg, "model", "gpt-4o"),
            temperature=getattr(sql_judge_cfg, "temperature", 0.0),
        )
        judges.append(
            SQLJudge(
                llm_client=llm_client,
                prompt_manager=prompt_manager,
                sql_client=sql_client,
                schema=schema,
                context=context,
            )
        )

    # Response Quality Judge
    rq_judge_cfg = getattr(eval_config, "response_quality_judge", None)
    if rq_judge_cfg and getattr(rq_judge_cfg, "enabled", False):
        llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=shared.llm.proxy_url,
            api_key=shared.llm.api_key,
            completion_model=getattr(rq_judge_cfg, "model", "gpt-4o"),
            temperature=getattr(rq_judge_cfg, "temperature", 0.0),
        )
        judges.append(
            ResponseQualityJudge(
                llm_client=llm_client,
                prompt_manager=prompt_manager,
                context=context,
            )
        )

    # Visualization Judge
    viz_judge_cfg = getattr(eval_config, "visualization_judge", None)
    if viz_judge_cfg and getattr(viz_judge_cfg, "enabled", False):
        llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=shared.llm.proxy_url,
            api_key=shared.llm.api_key,
            completion_model=getattr(viz_judge_cfg, "model", "gpt-4o"),
            temperature=getattr(viz_judge_cfg, "temperature", 0.0),
        )
        judges.append(
            VisualizationJudge(
                llm_client=llm_client,
                prompt_manager=prompt_manager,
            )
        )

    return judges


def create_invoke_fn():
    """Create invoke function using API endpoint."""
    api_config = eval_config.api
    endpoint = api_config.endpoint
    timeout = getattr(api_config, "timeout", 30)

    def invoke_fn(query: str, thread_id: str) -> dict:
        response = requests.post(
            endpoint,
            json={"query": query, "thread_id": thread_id, "include_tracing": True},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    return invoke_fn


def main():
    """Run evaluation."""
    logger.info("Starting Client BI Analytics Chatbot Evaluation")

    judges = create_judges()
    logger.info(f"Judges: {[j.name for j in judges]}")

    invoke_fn = create_invoke_fn()
    loader = DatasetLoader()

    runner = EvaluationRunner(
        invoke_fn=invoke_fn,
        judges=judges,
        dataset_loader=loader,
    )

    all_results = []
    for judge in judges:
        judge_cfg = getattr(eval_config, f"{judge.name}_judge", None)
        if not judge_cfg:
            continue
        dataset_path = getattr(judge_cfg, "dataset_path", None)
        pass_score = getattr(judge_cfg, "pass_score", 0.7)

        if not dataset_path:
            continue

        logger.info(f"Running {judge.name} evaluation on {dataset_path}")

        config = EvaluationConfig(
            chatbot="client",
            dataset_path=dataset_path,
            judges=[judge.name],
            pass_threshold=pass_score,
        )

        summary = runner.run(config)
        all_results.append((judge.name, summary))

    print("\n" + "=" * 60)
    print("Client BI Analytics Chatbot Evaluation Summary")
    print("=" * 60)

    total_tests = 0
    total_passed = 0

    for judge_name, summary in all_results:
        print(f"\n{judge_name}:")
        print(f"  Tests: {summary.total_tests}")
        print(f"  Passed: {summary.passed_tests}")
        print(f"  Failed: {summary.failed_tests}")
        print(f"  Pass rate: {summary.pass_rate:.1%}")
        print(f"  Avg score: {summary.average_score:.2f}")

        total_tests += summary.total_tests
        total_passed += summary.passed_tests

    print("\n" + "-" * 60)
    if total_tests > 0:
        print(
            f"Overall: {total_passed}/{total_tests} passed ({total_passed / total_tests:.1%})"
        )
    else:
        print("No tests run")
    print("=" * 60)

    return 0 if total_passed == total_tests else 1


if __name__ == "__main__":
    sys.exit(main())
