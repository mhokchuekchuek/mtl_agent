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
        prompt_name: str,
        prompt_label: str = "latest",
        context: str = "",
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label
        self.context = context

    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult | None:
        """Evaluate response quality using LLM.

        Returns None if this judge should be skipped (no 'response_quality' key in expected).
        Use expected response_quality: "null" for negative case.
        """
        # Skip if no 'response_quality' key in expected
        if expected is None or "response_quality" not in expected:
            return None

        expected_quality = expected.get("response_quality")
        is_negative_case = expected_quality == "null"

        question = input_data.get("question", "")
        response = output_data.get("response", "")
        steps = output_data.get("steps", [])

        # Handle negative case: expected response_quality: "null"
        if is_negative_case:
            if not response:
                return JudgeResult(
                    score=1.0,
                    passed=True,
                    reasoning="Correctly did not generate response",
                )
            else:
                return JudgeResult(
                    score=0.0,
                    passed=False,
                    reasoning=f"Should not respond but generated: {response[:100]}",
                )

        if not response:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning="No response generated",
            )

        # Use LLM to evaluate
        prompt_template = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )
        prompt = prompt_template.compile(
            context=self.context,
            question=question,
            response=response,
            steps=json.dumps(steps, indent=2),
            expected=expected_quality,
        )

        llm_response = self.llm_client.generate(prompt)

        # Parse LLM response (strip markdown wrapper if present)
        try:
            cleaned_response = self._strip_markdown_json(llm_response)
            result = json.loads(cleaned_response)

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
                "expected_response": expected_quality,
                "extracted_response": response[:200],
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
