"""Search quality judge using LLM-as-Judge."""

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

    LLM extracts search results from chatbot execution steps and evaluates:
    - Relevance: Are the search results relevant to the query?
    - Coverage: Are the expected products found in results?
    """

    name = "search"
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
        """Evaluate search quality using LLM to extract and judge.

        Returns None if this judge should be skipped (no 'search_results' key in expected).
        Use expected search_results: "null" for negative case (should not search).
        """
        # Skip if no 'search_results' key in expected
        if expected is None or "search_results" not in expected:
            return None

        expected_results = expected.get("search_results")
        is_negative_case = expected_results == "null"

        question = input_data.get("question", "")
        steps = output_data.get("steps", [])

        # Extract only search tool calls to reduce token usage
        search_tool_calls = self._extract_tool_calls(
            steps, ["product_search", "similar_products"]
        )

        # Use LLM to extract and evaluate
        prompt_template = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )
        prompt = prompt_template.compile(
            question=question,
            expected_results=json.dumps(expected_results)
            if not is_negative_case
            else "null (should not search)",
            steps=json.dumps(search_tool_calls, indent=2),
        )

        llm_response = self.llm_client.generate(prompt)

        # Parse LLM response (strip markdown wrapper if present)
        try:
            cleaned_response = self._strip_markdown_json(llm_response)
            result = json.loads(cleaned_response)
            extracted_results = result.get("extracted_results", [])

            # Handle negative case: expected search_results: "null"
            if is_negative_case:
                if not extracted_results:
                    return JudgeResult(
                        score=1.0,
                        passed=True,
                        reasoning="Correctly did not perform search",
                    )
                else:
                    return JudgeResult(
                        score=0.0,
                        passed=False,
                        reasoning=f"Should not search but found: {extracted_results}",
                    )

            # Handle empty results case: expected search_results: []
            if expected_results == []:
                if not extracted_results:
                    return JudgeResult(
                        score=1.0,
                        passed=True,
                        reasoning="Correctly returned no results",
                    )
                else:
                    return JudgeResult(
                        score=0.0,
                        passed=False,
                        reasoning=f"Should return no results but found: {extracted_results}",
                    )

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
                "extracted_results": extracted_results,
                "relevance": {
                    "score": relevance.score,
                    "reasoning": relevance.reasoning,
                },
                "coverage": {"score": coverage.score, "reasoning": coverage.reasoning},
            },
        )
