"""Evaluation entities (dataclasses)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EvaluationStrategy(str, Enum):
    """Evaluation strategy types."""

    FINAL_RESPONSE = "final_response"
    TRAJECTORY = "trajectory"
    SINGLE_STEP = "single_step"


@dataclass
class JudgeResult:
    """Result from a judge evaluation."""

    score: float
    passed: bool
    reasoning: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Turn:
    """A single turn in a multi-turn test case."""

    input: dict[str, Any]
    expected_output: dict[str, Any]


@dataclass
class TestCase:
    """A single test case for evaluation."""

    id: str
    input: dict[str, Any] | None = None
    expected_output: dict[str, Any] | None = None
    turns: list[Turn] | None = None
    tags: list[str] = field(default_factory=list)

    def is_multi_turn(self) -> bool:
        """Check if this is a multi-turn test case."""
        return self.turns is not None and len(self.turns) > 0


@dataclass
class EvaluationResult:
    """Complete evaluation result for a test case."""

    test_id: str
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    expected: dict[str, Any] | None
    judge_results: dict[str, JudgeResult]
    overall_score: float
    passed: bool
    trace_id: str | None = None
    latency_ms: float | None = None
