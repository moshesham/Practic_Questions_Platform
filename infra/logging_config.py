"""Logging utilities for question-specific file/console loggers."""

import logging
from pathlib import Path
import os
from datetime import datetime
from typing import Optional

from .exceptions import LoggingError, FileIOError


class LoggerManager:
    """Manage log directories and create configured loggers."""

    def __init__(self, base_dir: Optional[Path] = None, question_name: Optional[str] = None):
        """Initialize log directories for a given question.

        Args:
            base_dir: Project base directory; defaults to repository root.
            question_name: Optional question identifier to namespace logs.
            
        Raises:
            FileIOError: If log directories cannot be created.
        """

        # Use the calling script's directory as base if not provided
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent

        # Create logs directory
        self.logs_dir = self.base_dir / 'logs'
        try:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise FileIOError(f"Failed to create logs directory '{self.logs_dir}': {e}") from e

        # Create question-specific log directory if question name is provided
        self.question_log_dir = self.logs_dir / (question_name or 'general')
        try:
            self.question_log_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise FileIOError(f"Failed to create question log directory '{self.question_log_dir}': {e}") from e

    def create_logger(self, logger_name: str, log_level: int = logging.INFO) -> logging.Logger:
        """Create a logger with file and console handlers.

        Args:
            logger_name: Name of the logger.
            log_level: Logging level (default INFO).

        Returns:
            Configured ``logging.Logger`` instance.
            
        Raises:
            LoggingError: If logger creation fails.
        """

        try:
            logger = logging.getLogger(logger_name)
            logger.setLevel(log_level)

            # Create file handler
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = self.question_log_dir / f"{logger_name}_{timestamp}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Avoid duplicate handlers if create_logger called multiple times
            logger.handlers.clear()

            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            return logger
        except Exception as e:
            raise LoggingError(f"Failed to create logger '{logger_name}': {e}") from e