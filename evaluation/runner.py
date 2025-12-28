"""Evaluation runner for executing test cases."""

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

from evaluation.datasets.loader import DatasetLoader
from evaluation.entities import EvaluationResult, JudgeResult, TestCase
from evaluation.judges.base import BaseJudge
from libs.logger.logger import get_logger

logger = get_logger(__name__)


@dataclass
class EvaluationConfig:
    """Configuration for an evaluation run."""

    chatbot: str
    dataset_path: str
    judges: list[str] = field(default_factory=list)
    pass_threshold: float = 0.7


@dataclass
class EvaluationSummary:
    """Summary of evaluation results."""

    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    average_score: float
    results: list[EvaluationResult] = field(default_factory=list)


class EvaluationRunner:
    """Orchestrates evaluation of chatbot responses."""

    def __init__(
        self,
        invoke_fn: Callable[[str, str], dict],
        judges: list[BaseJudge],
        dataset_loader: DatasetLoader,
    ):
        """Initialize evaluation runner.

        Args:
            invoke_fn: Function to invoke chatbot (query, thread_id) -> response dict
            judges: List of judges to evaluate responses
            dataset_loader: Loader for test datasets
        """
        self.invoke_fn = invoke_fn
        self.judges = {j.name: j for j in judges}
        self.dataset_loader = dataset_loader

    def run(self, config: EvaluationConfig) -> EvaluationSummary:
        """Run evaluation on a dataset.

        Args:
            config: Evaluation configuration

        Returns:
            EvaluationSummary with results
        """
        test_cases = self.dataset_loader.load_dataset(config.dataset_path)
        logger.info(f"Loaded {len(test_cases)} test cases")

        # Filter judges
        active_judges = [
            self.judges[name] for name in config.judges if name in self.judges
        ]
        if not active_judges:
            active_judges = list(self.judges.values())
        logger.info(f"Using judges: {[j.name for j in active_judges]}")

        results = []
        for test_case in test_cases:
            try:
                if test_case.is_multi_turn():
                    result = self._run_multi_turn(test_case, active_judges, config)
                else:
                    result = self._run_single_turn(test_case, active_judges, config)
                results.append(result)
            except Exception as e:
                logger.error(f"Error running test case {test_case.id}: {e}")
                results.append(
                    EvaluationResult(
                        test_id=test_case.id,
                        input_data=test_case.input or {},
                        output_data={},
                        expected=test_case.expected_output,
                        judge_results={},
                        overall_score=0.0,
                        passed=False,
                    )
                )

        return self._create_summary(results, config.pass_threshold)

    def _run_single_turn(
        self,
        test_case: TestCase,
        judges: list[BaseJudge],
        config: EvaluationConfig,
    ) -> EvaluationResult:
        """Run a single-turn test case."""
        thread_id = f"eval-{uuid.uuid4().hex[:8]}"
        question = test_case.input.get("question", "")

        start_time = time.time()
        output = self.invoke_fn(question, thread_id)
        latency_ms = (time.time() - start_time) * 1000

        judge_results = {}
        for judge in judges:
            result = judge.evaluate(
                input_data=test_case.input,
                output_data=output,
                expected=test_case.expected_output,
            )
            judge_results[judge.name] = result

        overall_score = self._calculate_overall_score(judge_results)
        passed = overall_score >= config.pass_threshold

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
        config: EvaluationConfig,
    ) -> EvaluationResult:
        """Run a multi-turn test case."""
        thread_id = f"eval-{uuid.uuid4().hex[:8]}"
        all_judge_results = {}
        all_outputs = []
        total_latency = 0.0

        for i, turn in enumerate(test_case.turns):
            question = turn.input.get("question", "")

            start_time = time.time()
            output = self.invoke_fn(question, thread_id)
            total_latency += (time.time() - start_time) * 1000

            all_outputs.append(output)

            # Evaluate each turn
            for judge in judges:
                result = judge.evaluate(
                    input_data=turn.input,
                    output_data=output,
                    expected=turn.expected_output,
                )
                key = f"{judge.name}_turn_{i}"
                all_judge_results[key] = result

        overall_score = self._calculate_overall_score(all_judge_results)
        passed = overall_score >= config.pass_threshold

        return EvaluationResult(
            test_id=test_case.id,
            input_data={"turns": [t.input for t in test_case.turns]},
            output_data={"responses": all_outputs},
            expected={"turns": [t.expected_output for t in test_case.turns]},
            judge_results=all_judge_results,
            overall_score=overall_score,
            passed=passed,
            latency_ms=total_latency,
        )

    def _calculate_overall_score(self, judge_results: dict[str, JudgeResult]) -> float:
        """Calculate overall score from judge results."""
        if not judge_results:
            return 0.0
        scores = [r.score for r in judge_results.values()]
        return sum(scores) / len(scores)

    def _create_summary(
        self, results: list[EvaluationResult], threshold: float
    ) -> EvaluationSummary:
        """Create summary from results."""
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total - passed

        avg_score = sum(r.overall_score for r in results) / total if total > 0 else 0.0

        return EvaluationSummary(
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            pass_rate=passed / total if total > 0 else 0.0,
            average_score=avg_score,
            results=results,
        )
