"""SQL correctness judge using LLM-as-Judge."""

import json
from dataclasses import dataclass
from typing import Any

from evaluation.entities import EvaluationStrategy, JudgeResult
from evaluation.judges.base import BaseJudge
from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager


@dataclass
class SubScore:
    """Sub-score for a specific evaluation dimension."""

    score: float
    reasoning: str


class SQLJudge(BaseJudge):
    """Evaluates SQL query correctness using LLM-as-Judge.

    Evaluates:
    - Syntax: Is the SQL syntactically correct?
    - Correctness: Does it return the expected results?
    """

    name = "sql_correctness"
    strategy = EvaluationStrategy.SINGLE_STEP

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        sql_client: BaseSQLDatabase,
        schema: str,
        context: str = "",
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.sql_client = sql_client
        self.schema = schema
        self.context = context

    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult:
        """Evaluate SQL correctness."""
        expected_sql = expected.get("sql") if expected else None
        generated_sql = output_data.get("sql", "")

        # Handle negative case: sql should be null (should NOT generate SQL)
        if expected_sql is None:
            if not generated_sql:
                return JudgeResult(
                    score=1.0,
                    passed=True,
                    reasoning="Correctly refused to generate SQL",
                )
            else:
                return JudgeResult(
                    score=0.0,
                    passed=False,
                    reasoning=f"Should not generate SQL but generated: {generated_sql}",
                )

        # Expected SQL provided - should generate SQL
        if not generated_sql:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning="No SQL query generated",
            )

        # Execute both queries and compare results
        try:
            generated_results = self.sql_client.query(generated_sql)
        except Exception as e:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Generated SQL execution error: {e}",
                metadata={"generated_sql": generated_sql},
            )

        try:
            expected_results = self.sql_client.query(expected_sql)
        except Exception as e:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Expected SQL execution error: {e}",
                metadata={"expected_sql": expected_sql},
            )

        # Use LLM to evaluate
        question = input_data.get("question", "")
        prompt = self.prompt_manager.get_prompt(
            "evaluation_sql_judge",
            context=self.context,
            schema=self.schema,
            question=question,
            expected_sql=expected_sql,
            generated_sql=generated_sql,
            expected_results=json.dumps(expected_results[:10]),  # Limit for prompt size
            generated_results=json.dumps(generated_results[:10]),
        )

        llm_response = self.llm_client.complete(prompt)

        # Parse LLM response
        try:
            result = json.loads(llm_response)

            syntax = SubScore(
                score=float(result.get("syntax", {}).get("score", 0.0)),
                reasoning=result.get("syntax", {}).get("reasoning", ""),
            )
            correctness = SubScore(
                score=float(result.get("correctness", {}).get("score", 0.0)),
                reasoning=result.get("correctness", {}).get("reasoning", ""),
            )

            overall_score = (syntax.score + correctness.score) / 2

        except (json.JSONDecodeError, ValueError, TypeError):
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Failed to parse LLM response: {llm_response[:200]}",
            )

        return JudgeResult(
            score=overall_score,
            passed=overall_score >= 0.7,
            reasoning=f"Syntax: {syntax.score:.2f}, Correctness: {correctness.score:.2f}",
            metadata={
                "question": question,
                "expected_sql": expected_sql,
                "generated_sql": generated_sql,
                "expected_result_count": len(expected_results),
                "generated_result_count": len(generated_results),
                "syntax": {"score": syntax.score, "reasoning": syntax.reasoning},
                "correctness": {
                    "score": correctness.score,
                    "reasoning": correctness.reasoning,
                },
            },
        )
