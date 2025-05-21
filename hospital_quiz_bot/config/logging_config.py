"""
Logging configuration for the Hospital Quiz Bot.
This module configures the logging system for the bot.
"""

import logging
import logging.handlers
import os
from pathlib import Path

from .settings import settings

# Configure the logging system
LOGS_DIR = Path(__file__).parent.parent / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logging():
    """Set up the logging configuration."""
    # Get the log level from settings
    log_level = getattr(logging, settings.log_level)
    
    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Create a file handler for the bot logger
    file_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "bot.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    
    # Add the file handler to the bot logger
    bot_logger = logging.getLogger("hospital_quiz_bot")
    bot_logger.setLevel(log_level)
    bot_logger.addHandler(file_handler)
    
    # Create a separate file handler for errors
    error_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "errors.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    
    # Add the error handler to the root logger
    logging.getLogger().addHandler(error_handler)
    
    # Configure external loggers to reduce noise
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    # Log that the logging system has been configured
    bot_logger.info("Logging system configured")
    
    return bot_logger


# Create a logger instance for the bot
logger = setup_logging() 