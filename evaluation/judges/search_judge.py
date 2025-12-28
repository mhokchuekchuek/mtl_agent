"""Search quality judge for vector search evaluation using LLM."""

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


class SearchJudge(BaseJudge):
    """Evaluates vector search quality using LLM-as-Judge.

    Evaluates:
    - Relevance: Are the search results relevant to the query?
    - Coverage: Are the expected products found in results?
    """

    name = "search_quality"
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
        """Evaluate search quality using LLM."""
        expected_results = expected.get("search_results") if expected else None

        # If no expected search_results, skip
        if expected_results is None:
            return JudgeResult(
                score=1.0,
                passed=True,
                reasoning="No search_results check required for this test case",
            )

        question = input_data.get("question", "")
        actual_results = output_data.get("search_results", [])

        # Handle negative case: empty list expected
        if expected_results == []:
            if not actual_results:
                return JudgeResult(
                    score=1.0,
                    passed=True,
                    reasoning="Correctly returned no results",
                )
            else:
                return JudgeResult(
                    score=0.0,
                    passed=False,
                    reasoning=f"Should return no results but returned: {actual_results}",
                )

        if not actual_results:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning="No search results returned",
            )

        # Use LLM to evaluate
        prompt = self.prompt_manager.get_prompt(
            "evaluation_search_judge",
            question=question,
            expected_results=json.dumps(expected_results),
            actual_results=json.dumps(actual_results[:10]),  # Limit for prompt size
        )

        llm_response = self.llm_client.complete(prompt)

        # Parse LLM response
        try:
            result = json.loads(llm_response)

            relevance = SubScore(
                score=float(result.get("relevance", {}).get("score", 0.0)),
                reasoning=result.get("relevance", {}).get("reasoning", ""),
            )
            coverage = SubScore(
                score=float(result.get("coverage", {}).get("score", 0.0)),
                reasoning=result.get("coverage", {}).get("reasoning", ""),
            )

            overall_score = (relevance.score + coverage.score) / 2

        except (json.JSONDecodeError, ValueError, TypeError):
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Failed to parse LLM response: {llm_response[:200]}",
            )

        return JudgeResult(
            score=overall_score,
            passed=overall_score >= 0.6,
            reasoning=f"Relevance: {relevance.score:.2f}, Coverage: {coverage.score:.2f}",
            metadata={
                "question": question,
                "expected_results": expected_results,
                "actual_results": actual_results[:10],
                "relevance": {
                    "score": relevance.score,
                    "reasoning": relevance.reasoning,
                },
                "coverage": {"score": coverage.score, "reasoning": coverage.reasoning},
            },
        )
