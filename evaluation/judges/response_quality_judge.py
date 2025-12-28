"""Response quality judge using LLM-as-Judge."""

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


class ResponseQualityJudge(BaseJudge):
    """Evaluates response quality using LLM-as-Judge pattern.

    Evaluates two dimensions:
    - Relevance: Does the response address the question?
    - Faithfulness: Is the response grounded in facts (no hallucination)?
    """

    name = "response_quality"
    strategy = EvaluationStrategy.FINAL_RESPONSE

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        context: str = "",
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.context = context

    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult:
        """Evaluate response quality using LLM."""
        question = input_data.get("question", "")
        response = output_data.get("response", "")
        expected_quality = expected.get("response_quality") if expected else None

        # If no expected_quality defined, skip this judge
        if expected_quality is None:
            return JudgeResult(
                score=1.0,
                passed=True,
                reasoning="No response_quality check required for this test case",
            )

        if not response:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning="No response generated",
            )

        # Use LLM to evaluate
        prompt = self.prompt_manager.get_prompt(
            "evaluation_response_quality_judge",
            context=self.context,
            question=question,
            response=response,
            expected=expected_quality,
        )

        llm_response = self.llm_client.complete(prompt)

        # Parse LLM response - expects JSON with sub-scores
        try:
            result = json.loads(llm_response)

            relevance = SubScore(
                score=float(result.get("relevance", {}).get("score", 0.0)),
                reasoning=result.get("relevance", {}).get("reasoning", ""),
            )
            faithfulness = SubScore(
                score=float(result.get("faithfulness", {}).get("score", 0.0)),
                reasoning=result.get("faithfulness", {}).get("reasoning", ""),
            )

            # Overall score is average of sub-scores
            overall_score = (relevance.score + faithfulness.score) / 2

        except (json.JSONDecodeError, ValueError, TypeError):
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Failed to parse LLM response: {llm_response[:200]}",
            )

        return JudgeResult(
            score=overall_score,
            passed=overall_score >= 0.7,
            reasoning=f"Relevance: {relevance.score:.2f}, Faithfulness: {faithfulness.score:.2f}",
            metadata={
                "question": question,
                "response": response[:200],
                "expected": expected_quality,
                "relevance": {
                    "score": relevance.score,
                    "reasoning": relevance.reasoning,
                },
                "faithfulness": {
                    "score": faithfulness.score,
                    "reasoning": faithfulness.reasoning,
                },
            },
        )
