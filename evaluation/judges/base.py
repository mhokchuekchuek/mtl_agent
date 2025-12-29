"""Base judge interface."""

import re
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

    def _strip_markdown_json(self, text: str) -> str:
        """Strip markdown code block wrapper from JSON response.

        LLMs often return JSON wrapped in ```json ... ``` blocks.
        This helper extracts the raw JSON content.
        """
        text = text.strip()

        # Match complete ```json ... ``` or ``` ... ```
        pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
        match = re.match(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Handle case where opening ``` exists but no closing (truncated)
        if text.startswith("```"):
            # Remove opening ```json or ```
            text = re.sub(r"^```(?:json)?\s*\n?", "", text)
            return text.strip()

        return text

    def _extract_tool_calls(
        self, steps: list[dict], tool_names: list[str]
    ) -> list[dict]:
        """Extract only relevant tool calls from steps to reduce token usage.

        Args:
            steps: List of execution steps from chatbot
            tool_names: List of tool names to extract (e.g., ["sql_query"])

        Returns:
            List of tool call dicts with name, input, output
        """
        tool_calls = []
        for step in steps:
            # Check direct tool call in step
            if step.get("name") in tool_names:
                tool_calls.append(
                    {
                        "name": step.get("name"),
                        "input": step.get("input"),
                        "output": step.get("output"),
                    }
                )
            # Check nested tool_calls in step (from agents)
            for tc in step.get("tool_calls", []):
                if tc.get("name") in tool_names:
                    tool_calls.append(
                        {
                            "name": tc.get("name"),
                            "input": tc.get("input"),
                            "output": tc.get("output"),
                        }
                    )
        return tool_calls
