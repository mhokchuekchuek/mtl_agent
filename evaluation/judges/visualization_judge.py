"""Visualization judge using LLM-as-Judge."""

import json
from dataclasses import dataclass
from typing import Any

from evaluation.entities import EvaluationStrategy, JudgeResult
from evaluation.judges.base import BaseJudge
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager


@dataclass
class SubScore:
    """Sub-score for a specific evaluation dimension."""

    score: float
    reasoning: str


class VisualizationJudge(BaseJudge):
    """Evaluates visualization generation quality using LLM.

    Evaluates:
    - Appropriateness: Is a chart appropriate for this query?
    - Chart type: Is the chart type suitable for the data?
    """

    name = "visualization"
    strategy = EvaluationStrategy.SINGLE_STEP

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager

    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult:
        """Evaluate visualization quality using LLM."""
        if expected is None:
            return JudgeResult(
                score=1.0,
                passed=True,
                reasoning="No visualization check required for this test case",
            )

        expected_has_chart = expected.get("has_chart")
        expected_chart_type = expected.get("chart_type")

        # If no visualization expectations, skip
        if expected_has_chart is None and expected_chart_type is None:
            return JudgeResult(
                score=1.0,
                passed=True,
                reasoning="No visualization check required for this test case",
            )

        question = input_data.get("question", "")
        response = output_data.get("response", "")
        actual_has_chart = output_data.get("has_chart", False)
        actual_chart_type = output_data.get("chart_type", "")
        chart_data = output_data.get("chart_data", {})

        # Use LLM to evaluate
        prompt = self.prompt_manager.get_prompt(
            "evaluation_visualization_judge",
            question=question,
            response=response,
            expected_has_chart=expected_has_chart,
            expected_chart_type=expected_chart_type,
            actual_has_chart=actual_has_chart,
            actual_chart_type=actual_chart_type,
            chart_data=json.dumps(chart_data) if chart_data else "None",
        )

        llm_response = self.llm_client.complete(prompt)

        # Parse LLM response - expects JSON with sub-scores
        try:
            result = json.loads(llm_response)

            appropriateness = SubScore(
                score=float(result.get("appropriateness", {}).get("score", 0.0)),
                reasoning=result.get("appropriateness", {}).get("reasoning", ""),
            )
            chart_type_score = SubScore(
                score=float(result.get("chart_type", {}).get("score", 0.0)),
                reasoning=result.get("chart_type", {}).get("reasoning", ""),
            )

            overall_score = (appropriateness.score + chart_type_score.score) / 2

        except (json.JSONDecodeError, ValueError, TypeError):
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Failed to parse LLM response: {llm_response[:200]}",
            )

        return JudgeResult(
            score=overall_score,
            passed=overall_score >= 0.7,
            reasoning=f"Appropriateness: {appropriateness.score:.2f}, Chart type: {chart_type_score.score:.2f}",
            metadata={
                "question": question,
                "expected_has_chart": expected_has_chart,
                "actual_has_chart": actual_has_chart,
                "expected_chart_type": expected_chart_type,
                "actual_chart_type": actual_chart_type,
                "appropriateness": {
                    "score": appropriateness.score,
                    "reasoning": appropriateness.reasoning,
                },
                "chart_type": {
                    "score": chart_type_score.score,
                    "reasoning": chart_type_score.reasoning,
                },
            },
        )
