"""Judge selector for dynamic judge provider selection."""

from libs.base.selector import BaseToolSelector


class JudgeSelector(BaseToolSelector):
    """Selector for evaluation judges.

    Example:
        >>> judge = JudgeSelector.create(
        ...     provider="sql",
        ...     llm_client=llm_client,
        ...     prompt_manager=prompt_manager,
        ...     sql_client=sql_client,
        ...     schema=schema,
        ...     prompt_name="evaluation_sql_judge",
        ... )
    """

    _PROVIDERS = {
        "sql": "evaluation.judges.sql.main.SQLJudge",
        "search": "evaluation.judges.search.main.SearchJudge",
        "response_quality": "evaluation.judges.response_quality.main.ResponseQualityJudge",
        "visualization": "evaluation.judges.visualization.main.VisualizationJudge",
    }
