# utils/logging_utils.py
import logging
import json
import os
from typing import Any


def setup_logging():
    """Configure logging with env-driven level and file path.
    Env vars:
      - LOG_LEVEL: DEBUG|INFO|WARNING|ERROR|CRITICAL (default INFO)
      - LOG_FILE: Path to log file (default 'vignette_generation.log')
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    log_file = os.getenv("LOG_FILE", "vignette_generation.log")
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')

    root = logging.getLogger()
    root.setLevel(level)

    # Reset handlers to avoid duplicates if called multiple times
    root.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(stream_handler)


def log_dict(obj: Any) -> str:
    """Helper function to pretty print dictionaries/objects for logging"""
    if hasattr(obj, '__dict__'):
        return json.dumps(obj.__dict__, indent=2)
    return str(obj)
