import logging
from pathlib import Path

from infra.logging_config import LoggerManager


def test_logger_creation_creates_file(tmp_path: Path):
    manager = LoggerManager(base_dir=tmp_path, question_name="test_q")
    logger = manager.create_logger("test_logger")

    # Ensure log directory exists
    assert manager.question_log_dir.exists()
    assert manager.question_log_dir.is_dir()

    # Handlers should be attached
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    # A log file should be created after emitting a message
    logger.info("hello")
    log_files = list(manager.question_log_dir.glob("test_logger_*.log"))
    assert len(log_files) == 1


def test_logger_respects_custom_level(tmp_path: Path):
    manager = LoggerManager(base_dir=tmp_path, question_name="test_q")
    logger = manager.create_logger("level_logger", log_level=logging.WARNING)
    assert logger.level == logging.WARNING
