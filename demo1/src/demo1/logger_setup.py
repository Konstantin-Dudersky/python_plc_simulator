"""Настройка логгирования."""

import logging
import sys

import async_state_machine
import python_plc_simulator
from loguru import logger

logger.enable(python_plc_simulator.__name__)
logger.enable(async_state_machine.__name__)

logger.remove()
logger.add(sys.stderr, level="DEBUG")


class InterceptHandler(logging.Handler):
    """Подключить логи из модуля logging."""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # pyright: ignore
            frame = frame.f_back  # pyright: ignore
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
