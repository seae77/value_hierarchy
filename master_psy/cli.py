import argparse
import os
import logging

from utils.logging_utils import setup_logging
from master_psy.pipeline import main as run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate vignettes and questions for value pairs using OpenAI.",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        help="Directory to save generated PDFs (defaults to environment OUTPUT_DIR or 'output').",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default INFO).",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        default=None,
        help="Path to log file (default vignette_generation.log).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Set env vars for the underlying code to read
    if args.output_dir:
        os.environ["OUTPUT_DIR"] = args.output_dir
    if args.log_level:
        os.environ["LOG_LEVEL"] = args.log_level
    if args.log_file:
        os.environ["LOG_FILE"] = args.log_file

    # Initialize logging per env
    setup_logging()
    logging.getLogger(__name__).info("Starting vignette generation pipeline via CLI")

    # Delegate to existing main()
    run_pipeline()


if __name__ == "__main__":
    main()

