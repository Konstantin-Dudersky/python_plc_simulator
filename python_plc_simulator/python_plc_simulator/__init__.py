"""Инициализация пакета."""

from loguru import logger

from . import modbus_client, models

__all__ = [
    "modbus_client",
    "models",
]

logger.disable(__name__)
