"""SQL correctness judge using LLM-as-Judge with real query execution."""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from evaluation.entities import EvaluationStrategy, JudgeResult
from evaluation.judges.base import BaseJudge
from libs.database.sql.base import BaseSQLDatabase
from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SubScore:
    """Sub-score for a specific evaluation dimension."""

    score: float
    reasoning: str


class SQLJudge(BaseJudge):
    """Evaluates SQL query correctness by running queries and comparing results.

    Supports:
    - Single SQL query (string): sql: "SELECT..."
    - Multiple SQL statements (dict): sql: {"check_product": "SELECT...", "insert_order": "INSERT..."}
    - Multiple SQL tools: sql_query, place_order_sql

    1. Extract SQL from chatbot execution steps
    2. Run both expected and extracted SQL
    3. Send results to LLM for evaluation

    Scoring:
    - Result Match (70%): Do both queries return the same data?
    - Efficiency (30%): Is the SQL efficient?
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
        extractor_prompt_name: str = "evaluation_extractors_sql_extractor",
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.sql_client = sql_client
        self.schema = schema
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label
        self.context = context
        self.extractor_prompt_name = extractor_prompt_name

    def _execute_sql(self, sql: str) -> dict[str, Any]:
        """Execute SQL and return result with limited rows.

        Returns:
            Dict with 'data' (list of rows) and 'error' (if any)
        """
        try:
            result = self.sql_client.execute(sql)
            # Limit to first 20 rows to reduce token usage
            if isinstance(result, list):
                return {"data": result[:20], "row_count": len(result)}
            return {"data": result, "row_count": 1}
        except Exception as e:
            return {"data": None, "error": str(e)}

    def _extract_sql_operations(self, question: str, steps: list[dict]) -> dict:
        """Use LLM to extract SQL operations from steps.

        Step 1: Send steps to LLM to extract SQL and results.
        """
        extractor_prompt = self.prompt_manager.get_prompt(
            self.extractor_prompt_name, label=self.prompt_label
        )
        prompt = extractor_prompt.compile(
            question=question,
            steps=json.dumps(steps, indent=2, default=str),
        )

        response = self.llm_client.generate(prompt)

        try:
            cleaned = self._strip_markdown_json(response)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse extractor response: {response[:200]}")
            return {"sql_operations": []}

    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult | None:
        """Evaluate SQL correctness using 2-step LLM approach.

        Step 1: Extract SQL operations from steps using LLM
        Step 2: Evaluate extracted operations against expected

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

        # Step 1: Extract SQL operations using LLM
        extracted = self._extract_sql_operations(question, steps)
        sql_operations = extracted.get("sql_operations", [])

        # Handle negative case: expected sql: "null"
        if is_negative_case:
            if not sql_operations:
                return JudgeResult(
                    score=1.0,
                    passed=True,
                    reasoning="Correctly refused to generate SQL",
                )
            else:
                return JudgeResult(
                    score=0.0,
                    passed=False,
                    reasoning=f"Should not generate SQL but found: {len(sql_operations)} operations",
                    metadata={"sql_operations": sql_operations},
                )

        # Expected SQL provided - should have generated SQL
        if not sql_operations:
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning="No SQL operations found in execution steps",
            )

        # Run expected SQL to get expected result
        # sql: str -> run directly
        # sql: list -> run sequentially
        if isinstance(expected_sql, str):
            expected_result = self._execute_sql(expected_sql)
            expected_sql_str = expected_sql
        elif isinstance(expected_sql, list):
            expected_result = []
            for sql in expected_sql:
                expected_result.append(self._execute_sql(sql))
            expected_sql_str = json.dumps(expected_sql, indent=2)
        else:
            expected_result = None
            expected_sql_str = str(expected_sql)

        # Step 2: Use LLM to evaluate
        prompt_template = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )
        prompt = prompt_template.compile(
            current_date=datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%Y-%m-%d"),
            context=self.context,
            schema=self.schema,
            question=question,
            expected_sql=expected_sql_str,
            expected_result=json.dumps(expected_result, indent=2, default=str)
            if expected_result
            else "N/A",
            sql_operations=json.dumps(sql_operations, indent=2, default=str),
        )

        llm_response = self.llm_client.generate(prompt)

        # Parse LLM response
        try:
            cleaned_response = self._strip_markdown_json(llm_response)
            result = json.loads(cleaned_response)

            result_match = SubScore(
                score=float(result.get("result_match", {}).get("score", 0.0)),
                reasoning=result.get("result_match", {}).get("reasoning", ""),
            )
            efficiency = SubScore(
                score=float(result.get("efficiency", {}).get("score", 0.0)),
                reasoning=result.get("efficiency", {}).get("reasoning", ""),
            )

            # Weight: result_match 70%, efficiency 30%
            overall_score = result_match.score * 0.7 + efficiency.score * 0.3

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return JudgeResult(
                score=0.0,
                passed=False,
                reasoning=f"Failed to parse LLM response: {llm_response[:200]}",
            )

        return JudgeResult(
            score=overall_score,
            passed=overall_score >= 0.7,
            reasoning=f"Result Match: {result_match.score:.2f}, Efficiency: {efficiency.score:.2f}",
            metadata={
                "question": question,
                "expected_sql": expected_sql,
                "extracted_sql_operations": sql_operations,
                "result_match": {
                    "score": result_match.score,
                    "reasoning": result_match.reasoning,
                },
                "efficiency": {
                    "score": efficiency.score,
                    "reasoning": efficiency.reasoning,
                },
            },
        )
