"""Base evaluation repository interface."""

from abc import ABC, abstractmethod

from evaluation.entities import EvaluationResult


class BaseEvaluationRepository(ABC):
    """Abstract base class for evaluation repositories."""

    @abstractmethod
    def run(
        self,
        dataset_path: str,
        judge_names: list[str] | None = None,
    ) -> list[EvaluationResult]:
        """Run evaluation on a dataset.

        Args:
            dataset_path: Path to dataset
            judge_names: Optional list of judge names to use

        Returns:
            List of evaluation results
        """
        pass
