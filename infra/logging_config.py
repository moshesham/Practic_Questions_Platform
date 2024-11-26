# infra/logging_config.py
import logging
from pathlib import Path
import os
from datetime import datetime


class LoggerManager:
    def __init__(self, base_dir=None, question_name=None):
        # Use the calling script's directory as base if not provided
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent

        # Create logs directory
        self.logs_dir = self.base_dir / 'logs'
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Create question-specific log directory if question name is provided
        self.question_log_dir = self.logs_dir / (question_name or 'general')
        self.question_log_dir.mkdir(parents=True, exist_ok=True)

    def create_logger(self, logger_name, log_level=logging.INFO):
        # Create logger
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

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger