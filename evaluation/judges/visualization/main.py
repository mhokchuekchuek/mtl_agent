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

    LLM extracts visualization info from chatbot execution steps and evaluates:
    - Appropriateness: Is a chart appropriate for this query?
    - Chart type: Is the chart type suitable for the data?
    """

    name = "visualization"
    strategy = EvaluationStrategy.SINGLE_STEP

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str,
        prompt_label: str = "latest",
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label

    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult | None:
        """Evaluate visualization quality using LLM to extract and judge.

        Returns None if this judge should be skipped (no visualization keys in expected).
        Use expected has_chart: "null" for negative case (should not create chart).
        """
        # Skip if no visualization keys in expected
        if expected is None:
            return None

        expected_has_chart = expected.get("has_chart")
        expected_chart_type = expected.get("chart_type")

        # Skip if no visualization expectations
        if expected_has_chart is None and expected_chart_type is None:
            return None

        # Check if chart is NOT expected (false, "null", or False)
        is_negative_case = expected_has_chart in ("null", False, "false")

        question = input_data.get("question", "")
        response = output_data.get("response", "")
        steps = output_data.get("steps", [])

        # Extract only visualization tool calls to reduce token usage
        viz_tool_calls = self._extract_tool_calls(
            steps, ["create_visualization", "create_chart"]
        )

        # Handle negative case early: expected has_chart: false/null
        if is_negative_case:
            if not viz_tool_calls:
                return JudgeResult(
                    score=1.0,
                    passed=True,
                    reasoning="Correctly did not create visualization",
                )
            else:
                return JudgeResult(
                    score=0.0,
                    passed=False,
                    reasoning="Should not create chart but did",
                    metadata={"viz_tool_calls": viz_tool_calls},
                )

        # Use LLM to extract and evaluate
        prompt_template = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )
        prompt = prompt_template.compile(
            question=question,
            response=response,
            steps=json.dumps(viz_tool_calls, indent=2),
            expected_has_chart=expected_has_chart,
            expected_chart_type=expected_chart_type or "any",
        )

        llm_response = self.llm_client.generate(prompt)

        # Parse LLM response (strip markdown wrapper if present)
        try:
            cleaned_response = self._strip_markdown_json(llm_response)
            result = json.loads(cleaned_response)
            extracted_has_chart = result.get("extracted_has_chart", False)
            extracted_chart_type = result.get("extracted_chart_type")

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
                "extracted_has_chart": extracted_has_chart,
                "expected_chart_type": expected_chart_type,
                "extracted_chart_type": extracted_chart_type,
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
