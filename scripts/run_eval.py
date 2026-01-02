#!/usr/bin/env python3
"""Unified evaluation script for chatbots.

Usage:
    python scripts/run_eval.py customer
    python scripts/run_eval.py client
"""

import argparse
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from libs.logger.logger import get_logger, setup_logging

setup_logging(level="INFO")
logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run chatbot evaluation")
    parser.add_argument(
        "chatbot",
        choices=["customer", "client"],
        help="Chatbot to evaluate",
    )
    args = parser.parse_args()

    logger.info(f"Starting {args.chatbot} chatbot evaluation")

    # Import dependencies based on chatbot
    if args.chatbot == "customer":
        from evaluation.dependencies.customer import build_evaluation_service
    else:
        from evaluation.dependencies.client import build_evaluation_service

    # Build service
    service, dataset_path, results_path = build_evaluation_service()

    logger.info(f"Dataset path: {dataset_path}")

    # Run evaluation
    summary = service.run_evaluation(dataset_path)

    # Save summary CSV
    service.save_summary_csv(summary, results_path)

    # Print summary
    service.print_summary(summary)

    # Return exit code based on results
    return 0 if summary.passed_tests == summary.total_tests else 1


if __name__ == "__main__":
    sys.exit(main())
