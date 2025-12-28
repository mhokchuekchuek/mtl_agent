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
        """Load all test cases from a dataset path.

        Args:
            dataset_path: Full path from project root like "evaluation/datasets/customer/sql".

        Returns:
            List of TestCase objects from all YAML files in the path.
        """
        full_path = self.project_root / dataset_path
        if not full_path.exists():
            logger.warning(f"Dataset path not found: {full_path}")
            return []

        test_cases = []

        # Load from subdirectories (single_turn, multi_turn, negative)
        for subdir in ["single_turn", "multi_turn", "negative"]:
            subdir_path = full_path / subdir
            if subdir_path.exists():
                test_cases.extend(self._load_from_directory(subdir_path))

        # Also load any YAML files directly in the path
        test_cases.extend(self._load_from_directory(full_path, recursive=False))

        logger.info(f"Loaded {len(test_cases)} test cases from {dataset_path}")
        return test_cases

    def _load_from_directory(
        self, directory: Path, recursive: bool = True
    ) -> list[TestCase]:
        """Load test cases from YAML files in a directory.

        Args:
            directory: Directory path.
            recursive: Whether to search subdirectories.

        Returns:
            List of TestCase objects.
        """
        test_cases = []
        pattern = "**/*.yaml" if recursive else "*.yaml"

        for yaml_file in directory.glob(pattern):
            try:
                cases = self._load_yaml_file(yaml_file)
                test_cases.extend(cases)
            except Exception as e:
                logger.error(f"Error loading {yaml_file}: {e}")

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

    def list_datasets(self) -> list[str]:
        """List available dataset paths.

        Returns:
            List of dataset paths like ["customer/sql", "client/visualization"].
        """
        datasets = []

        for chatbot_dir in self.base_path.iterdir():
            if chatbot_dir.is_dir() and not chatbot_dir.name.startswith("_"):
                for category_dir in chatbot_dir.iterdir():
                    if category_dir.is_dir() and not category_dir.name.startswith("_"):
                        datasets.append(f"{chatbot_dir.name}/{category_dir.name}")

        return sorted(datasets)
