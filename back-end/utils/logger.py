# utils/logger.py

from loguru import logger

logger.add("app.log", rotation="1 MB", retention="10 days", level="DEBUG")

__all__ = ["logger"]
