"""Dataset loader for evaluation test cases."""

from pathlib import Path
from typing import Any

import yaml

from evaluation.entities import TestCase, Turn
from libs.logger.logger import get_logger

logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent


class DatasetLoader:
    """Load test cases from YAML dataset files."""

    def __init__(self, project_root: Path | None = None):
        """Initialize dataset loader.

        Args:
            project_root: Project root path. Defaults to mtl_agent/.
        """
        self.project_root = project_root or PROJECT_ROOT

    def load_dataset(self, dataset_path: str) -> list[TestCase]:
        """Load all test cases from a dataset path recursively.

        Scans all subdirectories (e.g., sql/, search/, response_quality/)
        and their turn type folders (single_turn/, multi_turn/, negative/).

        Args:
            dataset_path: Path like "evaluation/datasets/customer".

        Returns:
            List of TestCase objects from all YAML files.
        """
        full_path = self.project_root / dataset_path
        if not full_path.exists():
            logger.warning(f"Dataset path not found: {full_path}")
            return []

        test_cases = []

        # Recursively find all YAML files
        for yaml_file in full_path.rglob("*.yaml"):
            try:
                # Determine source_folder from path
                # e.g., customer/sql/single_turn/aggregation.yaml -> single_turn
                relative_path = yaml_file.relative_to(full_path)
                parts = relative_path.parts

                # Find turn type in path (single_turn, multi_turn, negative)
                source_folder = "single_turn"  # default
                for part in parts:
                    if part in ("single_turn", "multi_turn", "negative"):
                        source_folder = part
                        break

                cases = self._load_yaml_file(yaml_file)
                for case in cases:
                    case.source_folder = source_folder
                test_cases.extend(cases)

            except Exception as e:
                logger.error(f"Error loading {yaml_file}: {e}")

        logger.info(f"Loaded {len(test_cases)} test cases from {dataset_path}")
        return test_cases

    def _load_yaml_file(self, file_path: Path) -> list[TestCase]:
        """Load test cases from a single YAML file.

        Args:
            file_path: Path to YAML file.

        Returns:
            List of TestCase objects.
        """
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        if not data:
            return []

        test_cases = []
        raw_cases = data.get("test_cases", [])

        for raw in raw_cases:
            test_case = self._parse_test_case(raw)
            if test_case:
                test_cases.append(test_case)

        return test_cases

    def _parse_test_case(self, raw: dict[str, Any]) -> TestCase | None:
        """Parse a raw test case dict into TestCase object.

        Args:
            raw: Raw test case dictionary.

        Returns:
            TestCase object or None if invalid.
        """
        if not raw.get("id"):
            return None

        # Check if multi-turn
        if "turns" in raw:
            turns = []
            for turn_data in raw["turns"]:
                turn = Turn(
                    input=turn_data.get("input", {}),
                    expected_output=turn_data.get("expected_output", {}),
                )
                turns.append(turn)

            return TestCase(
                id=raw["id"],
                turns=turns,
            )
        else:
            # Single-turn
            return TestCase(
                id=raw["id"],
                input=raw.get("input", {}),
                expected_output=raw.get("expected_output", {}),
            )
