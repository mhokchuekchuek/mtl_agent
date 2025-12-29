"""Evaluation service use case."""

from evaluation.entities import EvaluationResult, EvaluationSummary
from evaluation.repositories.base import BaseEvaluationRepository
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class EvaluationService:
    """Service for running evaluations.

    Orchestrates evaluation runs and aggregates results.
    """

    def __init__(self, evaluation_repo: BaseEvaluationRepository):
        """Initialize evaluation service.

        Args:
            evaluation_repo: Repository for running evaluations
        """
        self.evaluation_repo = evaluation_repo

    def run_evaluation(self, dataset_path: str) -> EvaluationSummary:
        """Run evaluation on a dataset with all configured judges.

        All judges run on all test cases. Judges skip test cases
        where their expected fields are not present.

        Args:
            dataset_path: Path to dataset folder

        Returns:
            EvaluationSummary with results
        """
        logger.info(f"Running evaluation on {dataset_path}")

        results = self.evaluation_repo.run(dataset_path=dataset_path)

        summary = self._create_summary(
            results=results,
            dataset_path=dataset_path,
        )

        logger.info(
            f"Evaluation complete: {summary.passed_tests}/{summary.total_tests} passed "
            f"({summary.pass_rate:.1%})"
        )

        return summary

    def _create_summary(
        self,
        results: list[EvaluationResult],
        dataset_path: str,
    ) -> EvaluationSummary:
        """Create summary from results."""
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total - passed

        avg_score = sum(r.overall_score for r in results) / total if total > 0 else 0.0

        return EvaluationSummary(
            dataset_path=dataset_path,
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            pass_rate=passed / total if total > 0 else 0.0,
            average_score=avg_score,
            results=results,
        )

    def print_summary(self, summary: EvaluationSummary):
        """Print evaluation summary to console."""
        print("\n" + "=" * 60)
        print("Evaluation Summary")
        print("=" * 60)

        print(f"\nDataset: {summary.dataset_path}")
        print(f"Tests: {summary.total_tests}")
        print(f"Passed: {summary.passed_tests}")
        print(f"Failed: {summary.failed_tests}")
        print(f"Pass rate: {summary.pass_rate:.1%}")
        print(f"Avg score: {summary.average_score:.2f}")

        print("\n" + "-" * 60)
        print("Results by test case:")
        for result in summary.results:
            status = "PASS" if result.passed else "FAIL"
            print(f"  [{status}] {result.test_id}: {result.overall_score:.2f}")
            for judge_name, jr in result.judge_results.items():
                judge_status = "PASS" if jr.passed else "FAIL"
                print(f"      [{judge_status}] {judge_name}: {jr.score:.2f}")

        print("=" * 60)
