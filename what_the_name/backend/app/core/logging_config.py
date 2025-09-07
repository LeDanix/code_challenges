import logging
import sys
import os
from typing import Optional

class LoggerManager:
    _instances: dict[str, logging.Logger] = {}

    LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, log_file: Optional[str] = None, level: int = logging.DEBUG):
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "logs")
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = log_file or os.path.join(log_dir, "app.log")
        self.level = level

    def get_logger(self, name: str) -> logging.Logger:
        if name in self._instances:
            return self._instances[name]

        logger = logging.getLogger(name)
        logger.setLevel(self.level)

        if not logger.handlers:
            formatter = logging.Formatter(self.LOG_FORMAT, datefmt=self.DATE_FORMAT)

            # Consola
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # Archivo
            file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        self._instances[name] = logger
        return logger

# Use this variable to instanciate your log
logger_manager = LoggerManager()

if __name__ == "__main__":
    # --- Usage ---
    logger = logger_manager.get_logger(__name__)

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
