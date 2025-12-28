"""Base judge interface."""

from abc import ABC, abstractmethod
from typing import Any

from evaluation.entities import EvaluationStrategy, JudgeResult


class BaseJudge(ABC):
    """Abstract base class for evaluation judges."""

    name: str = "base_judge"
    strategy: EvaluationStrategy = EvaluationStrategy.FINAL_RESPONSE

    @abstractmethod
    def evaluate(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        expected: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeResult:
        """Evaluate agent output."""
        pass
