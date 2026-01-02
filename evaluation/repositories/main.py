"""Evaluation repository implementation."""

import time
import uuid
from datetime import datetime
from pathlib import Path

import requests
import yaml

from evaluation.entities import EvaluationResult, JudgeResult, TestCase, TurnResult
from evaluation.judges.base import BaseJudge
from evaluation.loader import DatasetLoader
from evaluation.repositories.base import BaseEvaluationRepository
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class EvaluationRepository(BaseEvaluationRepository):
    """Repository for running evaluations.

    Handles:
    - Invoking chatbot API
    - Running judges on responses
    - Saving results to disk with full sub-scores and LLM reasoning
    """

    def __init__(
        self,
        endpoint: str,
        timeout: int,
        judges: list[BaseJudge],
        dataset_loader: DatasetLoader,
        results_path: str,
        pass_threshold: float = 0.7,
        chatbot_name: str = "chatbot",
        project_root: Path | None = None,
    ):
        """Initialize evaluation repository.

        Args:
            endpoint: Chatbot API endpoint
            timeout: Request timeout in seconds
            judges: List of judges to evaluate responses
            dataset_loader: Loader for test datasets
            results_path: Base path for saving results
            pass_threshold: Score threshold for passing
            chatbot_name: Name of chatbot (for logging)
            project_root: Project root for saving results
        """
        self.endpoint = endpoint
        self.timeout = timeout
        self.judges = {j.name: j for j in judges}
        self.dataset_loader = dataset_loader
        self.results_path = results_path
        self.pass_threshold = pass_threshold
        self.chatbot_name = chatbot_name
        self.project_root = project_root or Path(__file__).parent.parent.parent

    def run(
        self,
        dataset_path: str,
        judge_names: list[str] | None = None,
    ) -> list[EvaluationResult]:
        """Run evaluation on a dataset."""
        test_cases = self.dataset_loader.load_dataset(dataset_path)
        logger.info(f"Loaded {len(test_cases)} test cases from {dataset_path}")

        # Filter judges
        if judge_names:
            active_judges = [
                self.judges[name] for name in judge_names if name in self.judges
            ]
        else:
            active_judges = list(self.judges.values())
        logger.info(f"Using judges: {[j.name for j in active_judges]}")

        # Setup results directory
        results_base_dir = self.project_root / self.results_path

        results = []
        for test_case in test_cases:
            try:
                if test_case.is_multi_turn():
                    result = self._run_multi_turn(test_case, active_judges)
                else:
                    result = self._run_single_turn(test_case, active_judges)
                results.append(result)

                # Save result immediately
                results_dir = results_base_dir / test_case.source_folder
                results_dir.mkdir(parents=True, exist_ok=True)
                self._save_result(result, results_dir)

            except Exception as e:
                logger.error(f"Error running test case {test_case.id}: {e}")
                error_result = EvaluationResult(
                    test_id=test_case.id,
                    input_data=test_case.input or {},
                    output_data={},
                    expected=test_case.expected_output,
                    judge_results={},
                    overall_score=0.0,
                    passed=False,
                )
                results.append(error_result)

                results_dir = results_base_dir / test_case.source_folder
                results_dir.mkdir(parents=True, exist_ok=True)
                self._save_result(error_result, results_dir, error=str(e))

        return results

    def _invoke_chatbot(self, query: str, thread_id: str, user_id: str = "1") -> dict:
        """Invoke chatbot API."""
        response = requests.post(
            self.endpoint,
            json={
                "query": query,
                "thread_id": thread_id,
                "user_id": user_id,
                "include_steps": True,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _run_single_turn(
        self,
        test_case: TestCase,
        judges: list[BaseJudge],
    ) -> EvaluationResult:
        """Run a single-turn test case."""
        thread_id = f"eval-{uuid.uuid4().hex[:8]}"
        question = test_case.input.get("question", "")

        start_time = time.time()
        output = self._invoke_chatbot(question, thread_id)
        latency_ms = (time.time() - start_time) * 1000

        judge_results = {}
        for judge in judges:
            result = judge.evaluate(
                input_data=test_case.input,
                output_data=output,
                expected=test_case.expected_output,
            )
            # Skip if judge returns None (no matching expected field)
            if result is not None:
                judge_results[judge.name] = result

        overall_score = self._calculate_overall_score(judge_results)
        passed = overall_score >= self.pass_threshold

        return EvaluationResult(
            test_id=test_case.id,
            input_data=test_case.input,
            output_data=output,
            expected=test_case.expected_output,
            judge_results=judge_results,
            overall_score=overall_score,
            passed=passed,
            trace_id=output.get("tracing", {}).get("trace_id"),
            latency_ms=latency_ms,
        )

    def _run_multi_turn(
        self,
        test_case: TestCase,
        judges: list[BaseJudge],
    ) -> EvaluationResult:
        """Run a multi-turn test case."""
        thread_id = f"eval-{uuid.uuid4().hex[:8]}"
        turn_results: list[TurnResult] = []
        all_judge_results = {}
        total_latency = 0.0

        for i, turn in enumerate(test_case.turns):
            question = turn.input.get("question", "")

            start_time = time.time()
            output = self._invoke_chatbot(question, thread_id)
            turn_latency = (time.time() - start_time) * 1000
            total_latency += turn_latency

            # Evaluate this turn
            turn_judge_results = {}
            for judge in judges:
                result = judge.evaluate(
                    input_data=turn.input,
                    output_data=output,
                    expected=turn.expected_output,
                )
                # Skip if judge returns None (no matching expected field)
                if result is not None:
                    turn_judge_results[judge.name] = result
                    # Also keep flat structure for overall score calculation
                    all_judge_results[f"{judge.name}_turn_{i}"] = result

            # Create turn result
            turn_result = TurnResult(
                turn=i,
                input_data=turn.input,
                output_data={
                    "response": output.get("response", ""),
                    "steps": output.get("steps", []),
                },
                expected=turn.expected_output,
                judge_results=turn_judge_results,
                latency_ms=turn_latency,
            )
            turn_results.append(turn_result)

        overall_score = self._calculate_overall_score(all_judge_results)
        passed = overall_score >= self.pass_threshold

        last_response = (
            turn_results[-1].output_data.get("response", "") if turn_results else ""
        )

        return EvaluationResult(
            test_id=test_case.id,
            input_data={"turns": [t.input for t in test_case.turns]},
            output_data={"response": last_response},
            expected={"turns": [t.expected_output for t in test_case.turns]},
            judge_results=all_judge_results,
            overall_score=overall_score,
            passed=passed,
            latency_ms=total_latency,
            turns=turn_results,
        )

    def _calculate_overall_score(self, judge_results: dict[str, JudgeResult]) -> float:
        """Calculate overall score from judge results."""
        if not judge_results:
            return 0.0
        scores = [r.score for r in judge_results.values()]
        return sum(scores) / len(scores)

    def _save_result(
        self,
        result: EvaluationResult,
        results_dir: Path,
        error: str | None = None,
    ):
        """Save result as results.yaml and detail.yaml in a folder."""
        folder_name = result.test_id
        result_folder = results_dir / folder_name
        result_folder.mkdir(parents=True, exist_ok=True)

        # Check if multi-turn
        if result.turns:
            results_data, detail_data = self._format_multi_turn_yaml(result)
        else:
            results_data, detail_data = self._format_single_turn_yaml(result)

        if error:
            results_data["error"] = error

        # Save results.yaml
        with open(result_folder / "results.yaml", "w") as f:
            yaml.dump(
                results_data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        # Save detail.yaml
        with open(result_folder / "detail.yaml", "w") as f:
            yaml.dump(
                detail_data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        logger.info(f"Result saved: {result_folder}")

    def _truncate(self, text: str, max_length: int = 200) -> str:
        """Truncate text with ellipsis if too long."""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    def _get_expected_actual(
        self, metadata: dict | None
    ) -> tuple[dict | None, dict | None]:
        """Extract expected and actual values from judge metadata.

        Looks for keys starting with 'expected_' and 'extracted_'.
        Returns (expected, actual) dicts with prefixes removed.
        """
        if not metadata:
            return None, None

        expected = {}
        actual = {}

        for key, value in metadata.items():
            if key.startswith("expected_"):
                clean_key = key.replace("expected_", "")
                expected[clean_key] = value
            elif key.startswith("extracted_"):
                clean_key = key.replace("extracted_", "")
                actual[clean_key] = value

        return expected or None, actual or None

    def _format_single_turn_yaml(self, result: EvaluationResult) -> tuple[dict, dict]:
        """Format single-turn result as results.yaml and detail.yaml."""
        # results.yaml - summary with truncated output
        results_data = {
            "test_id": result.test_id,
            "type": "single_turn",
            "passed": result.passed,
            "overall_score": round(result.overall_score, 2),
            "latency_ms": round(result.latency_ms, 0) if result.latency_ms else None,
            "timestamp": datetime.now().isoformat(),
            "input": result.input_data,
            "output": {
                "response": self._truncate(result.output_data.get("response", "")),
            },
            "expected": result.expected,
            "judge_results": {},
        }

        # Format judge results with expected/actual and sub_scores
        for name, jr in result.judge_results.items():
            judge_data = {
                "score": round(jr.score, 2),
                "passed": jr.passed,
            }

            # Add expected/actual values from metadata
            expected_vals, actual_vals = self._get_expected_actual(jr.metadata)
            if expected_vals:
                judge_data["expected"] = expected_vals
            if actual_vals:
                judge_data["actual"] = actual_vals

            # Add sub_scores if available
            if jr.metadata:
                sub_scores = {}
                for key, value in jr.metadata.items():
                    if isinstance(value, dict) and "score" in value:
                        sub_scores[key] = {
                            "score": round(value.get("score", 0), 2),
                            "reasoning": value.get("reasoning", ""),
                        }
                if sub_scores:
                    judge_data["sub_scores"] = sub_scores
            else:
                judge_data["reasoning"] = jr.reasoning

            results_data["judge_results"][name] = judge_data

        # detail.yaml - full output and steps
        detail_data = {
            "output": {
                "response": result.output_data.get("response", ""),
                "steps": result.output_data.get("steps", []),
            },
        }

        return results_data, detail_data

    def _format_multi_turn_yaml(self, result: EvaluationResult) -> tuple[dict, dict]:
        """Format multi-turn result as results.yaml and detail.yaml."""
        # results.yaml
        results_data = {
            "test_id": result.test_id,
            "type": "multi_turn",
            "passed": result.passed,
            "overall_score": round(result.overall_score, 2),
            "total_latency_ms": round(result.latency_ms, 0)
            if result.latency_ms
            else None,
            "timestamp": datetime.now().isoformat(),
            "turns": [],
        }

        # detail.yaml
        detail_data = {
            "turns": [],
        }

        for turn_result in result.turns:
            # Turn for results.yaml
            turn_summary = {
                "turn": turn_result.turn,
                "input": turn_result.input_data,
                "output": {
                    "response": self._truncate(
                        turn_result.output_data.get("response", "")
                    ),
                },
                "expected": turn_result.expected,
                "latency_ms": round(turn_result.latency_ms, 0),
                "judge_results": {},
            }

            # Format judge results with expected/actual and sub_scores
            for name, jr in turn_result.judge_results.items():
                judge_data = {
                    "score": round(jr.score, 2),
                    "passed": jr.passed,
                }

                # Add expected/actual values from metadata
                expected_vals, actual_vals = self._get_expected_actual(jr.metadata)
                if expected_vals:
                    judge_data["expected"] = expected_vals
                if actual_vals:
                    judge_data["actual"] = actual_vals

                # Add sub_scores if available
                if jr.metadata:
                    sub_scores = {}
                    for key, value in jr.metadata.items():
                        if isinstance(value, dict) and "score" in value:
                            sub_scores[key] = {
                                "score": round(value.get("score", 0), 2),
                                "reasoning": value.get("reasoning", ""),
                            }
                    if sub_scores:
                        judge_data["sub_scores"] = sub_scores
                else:
                    judge_data["reasoning"] = jr.reasoning

                turn_summary["judge_results"][name] = judge_data

            results_data["turns"].append(turn_summary)

            # Turn for detail.yaml
            turn_detail = {
                "turn": turn_result.turn,
                "output": {
                    "response": turn_result.output_data.get("response", ""),
                    "steps": turn_result.output_data.get("steps", []),
                },
            }
            detail_data["turns"].append(turn_detail)

        return results_data, detail_data

    def _format_single_turn_result(self, result: EvaluationResult) -> dict:
        """Format single-turn result for saving."""
        return {
            "timestamp": datetime.now().isoformat(),
            "chatbot": self.chatbot_name,
            "test_id": result.test_id,
            "type": "single_turn",
            "passed": result.passed,
            "overall_score": result.overall_score,
            "latency_ms": result.latency_ms,
            "input": result.input_data,
            "output": {
                "response": result.output_data.get("response", ""),
                "steps": result.output_data.get("steps", []),
            },
            "expected": result.expected,
            "judge_results": {
                name: {
                    "score": jr.score,
                    "passed": jr.passed,
                    "reasoning": jr.reasoning,
                    "sub_scores": jr.metadata,
                }
                for name, jr in result.judge_results.items()
            },
        }

    def _format_multi_turn_result(self, result: EvaluationResult) -> dict:
        """Format multi-turn result for saving with per-turn structure."""
        turns_data = []
        for turn_result in result.turns:
            turn_data = {
                "turn": turn_result.turn,
                "input": turn_result.input_data,
                "output": turn_result.output_data,
                "expected": turn_result.expected,
                "latency_ms": turn_result.latency_ms,
                "judge_results": {
                    name: {
                        "score": jr.score,
                        "passed": jr.passed,
                        "reasoning": jr.reasoning,
                        "sub_scores": jr.metadata,
                    }
                    for name, jr in turn_result.judge_results.items()
                },
            }
            turns_data.append(turn_data)

        return {
            "timestamp": datetime.now().isoformat(),
            "chatbot": self.chatbot_name,
            "test_id": result.test_id,
            "type": "multi_turn",
            "passed": result.passed,
            "overall_score": result.overall_score,
            "total_latency_ms": result.latency_ms,
            "turns": turns_data,
        }
