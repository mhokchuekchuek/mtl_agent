#!/usr/bin/env python3
"""Unified evaluation script for chatbots.

Usage:
    # Run all tests for a chatbot
    python scripts/run_eval.py customer
    python scripts/run_eval.py client

    # Run specific directory
    python scripts/run_eval.py customer --path data/eval_datasets/customer/browse_products

    # Run single yaml file
    python scripts/run_eval.py customer --path data/eval_datasets/customer/browse_products/single_turn/search.yaml

    # Run multiple paths
    python scripts/run_eval.py customer --path data/eval_datasets/customer/browse_products --path data/eval_datasets/customer/place_order
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
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        help="Dataset path(s) to evaluate. Can be directory or yaml file. "
        "Use multiple --path flags for multiple paths. "
        "If not specified, uses default dataset path from config.",
    )
    args = parser.parse_args()

    logger.info(f"Starting {args.chatbot} chatbot evaluation")

    # Import dependencies based on chatbot
    if args.chatbot == "customer":
        from evaluation.dependencies.customer import build_evaluation_service
    else:
        from evaluation.dependencies.client import build_evaluation_service

    # Build service
    service, default_dataset_path, results_path = build_evaluation_service()

    # Determine dataset path(s)
    if args.paths:
        # Single path or list of paths
        dataset_path = args.paths[0] if len(args.paths) == 1 else args.paths
        logger.info(f"Using custom path(s): {dataset_path}")
    else:
        dataset_path = default_dataset_path
        logger.info(f"Using default dataset path: {dataset_path}")

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
