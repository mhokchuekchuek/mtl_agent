"""Evaluation service use case."""

import csv
from pathlib import Path

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

    def save_summary_csv(self, summary: EvaluationSummary, results_path: str):
        """Save evaluation summary as CSV.

        Args:
            summary: Evaluation summary with results
            results_path: Path to save summary.csv
        """
        results_dir = Path(results_path)
        results_dir.mkdir(parents=True, exist_ok=True)
        csv_path = results_dir / "summary.csv"

        # Collect all judge names from results
        all_judges = set()
        for result in summary.results:
            for judge_name in result.judge_results.keys():
                # Remove turn suffix for multi-turn (e.g., sql_turn_0 -> sql)
                base_name = judge_name.split("_turn_")[0]
                all_judges.add(base_name)

        judge_columns = sorted(all_judges)

        # Write CSV
        with open(csv_path, "w", newline="") as f:
            fieldnames = [
                "test_id",
                "turn_type",
                "passed",
                "overall_score",
                "latency_ms",
            ] + [f"{j}_score" for j in judge_columns]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in summary.results:
                # Determine turn_type from test structure
                if result.turns:
                    turn_type = "multi_turn"
                elif any(
                    jr.metadata.get("is_negative")
                    for jr in result.judge_results.values()
                ):
                    turn_type = "negative"
                else:
                    turn_type = "single_turn"

                row = {
                    "test_id": result.test_id,
                    "turn_type": turn_type,
                    "passed": result.passed,
                    "overall_score": round(result.overall_score, 2),
                    "latency_ms": round(result.latency_ms) if result.latency_ms else "",
                }

                # Add judge scores (average across turns for multi-turn)
                for judge in judge_columns:
                    scores = []
                    for jname, jr in result.judge_results.items():
                        if jname == judge or jname.startswith(f"{judge}_turn_"):
                            scores.append(jr.score)
                    if scores:
                        row[f"{judge}_score"] = round(sum(scores) / len(scores), 2)
                    else:
                        row[f"{judge}_score"] = ""

                writer.writerow(row)

        logger.info(f"Summary CSV saved: {csv_path}")

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
