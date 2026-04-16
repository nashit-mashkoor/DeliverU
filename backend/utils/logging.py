import logging
import sys
from typing import Any, Dict, Optional

from backend.utils.singleton import Singleton


class Logging(metaclass=Singleton):
    """Singleton logger configuration"""

    def __init__(self):
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configure and return a logger instance"""
        logger = logging.getLogger("backend")

        if not logger.handlers:
            logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(extra_data)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def get_logger(self) -> "StructuredLogger":
        """Get the configured logger with structured logging support"""
        return StructuredLogger(self.logger)


class StructuredLogger:
    """Wrapper for structured logging with extra data"""

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def _log(self, level: int, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log with structured extra data"""
        extra_data = extra or {}
        extra_str = str(extra_data) if extra_data else "{}"
        self._logger.log(level, msg, extra={"extra_data": extra_str})

    def debug(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.DEBUG, msg, extra)

    def info(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.INFO, msg, extra)

    def warning(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.WARNING, msg, extra)

    def error(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.ERROR, msg, extra)

    def critical(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.CRITICAL, msg, extra)

