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

    LLM extracts SQL from chatbot execution steps and evaluates:
    - Syntax: Is the SQL syntactically correct?
    - Correctness: Does it match the expected SQL logic?
    """

    name = "sql"
    strategy = EvaluationStrategy.SINGLE_STEP

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        sql_client: BaseSQLDatabase,
        schema: str,
        prompt_name: str,
        prompt_label: str = "latest",
        context: str = "",
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.sql_client = sql_client
        self.schema = schema
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
        """Evaluate SQL correctness using LLM to extract and judge.

        Returns None if this judge should be skipped (no 'sql' key in expected).
        Use expected sql: "null" for negative case (should not generate SQL).
        """
        # Skip if no 'sql' key in expected
        if expected is None or "sql" not in expected:
            return None

        expected_sql = expected.get("sql")
        is_negative_case = expected_sql == "null"

        question = input_data.get("question", "")
        steps = output_data.get("steps", [])

        # Extract only sql_query tool calls to reduce token usage
        sql_tool_calls = self._extract_tool_calls(steps, ["sql_query"])

        # Use LLM to extract SQL and evaluate
        prompt_template = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )
        prompt = prompt_template.compile(
            context=self.context,
            schema=self.schema,
            question=question,
            expected_sql=expected_sql
            if not is_negative_case
            else "null (should not generate SQL)",
            steps=json.dumps(sql_tool_calls, indent=2),
        )

        llm_response = self.llm_client.generate(prompt)

        # Parse LLM response (strip markdown wrapper if present)
        try:
            cleaned_response = self._strip_markdown_json(llm_response)
            result = json.loads(cleaned_response)
            extracted_sql = result.get("extracted_sql")

            # Handle negative case: expected sql: "null"
            if is_negative_case:
                if not extracted_sql:
                    return JudgeResult(
                        score=1.0,
                        passed=True,
                        reasoning="Correctly refused to generate SQL",
                    )
                else:
                    return JudgeResult(
                        score=0.0,
                        passed=False,
                        reasoning=f"Should not generate SQL but generated: {extracted_sql}",
                        metadata={"extracted_sql": extracted_sql},
                    )

            # Expected SQL provided - should have generated SQL
            if not extracted_sql:
                return JudgeResult(
                    score=0.0,
                    passed=False,
                    reasoning="No SQL query found in execution steps",
                )

            syntax = SubScore(
                score=float(result.get("syntax", {}).get("score", 0.0)),
                reasoning=result.get("syntax", {}).get("reasoning", ""),
            )
            correctness = SubScore(
                score=float(result.get("correctness", {}).get("score", 0.0)),
                reasoning=result.get("correctness", {}).get("reasoning", ""),
            )

            overall_score = (syntax.score + correctness.score) / 2

        except (json.JSONDecodeError, ValueError, TypeError) as e:
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
                "extracted_sql": extracted_sql,
                "syntax": {"score": syntax.score, "reasoning": syntax.reasoning},
                "correctness": {
                    "score": correctness.score,
                    "reasoning": correctness.reasoning,
                },
            },
        )
