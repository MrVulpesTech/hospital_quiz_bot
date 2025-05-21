"""
Main entry point for the Hospital Quiz Bot.
This module initializes the bot and starts polling.
"""

import asyncio
import logging
import sys
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties

from hospital_quiz_bot.config.settings import settings
from hospital_quiz_bot.config.logging_config import logger
from hospital_quiz_bot.app.database.connection import init_db, close_db, get_session, async_session_factory
from hospital_quiz_bot.app.handlers import commands, quiz, report


# Create a proper async context manager for the session
@asynccontextmanager
async def session_pool():
    """Provide a session from the pool."""
    async with async_session_factory() as session:
        yield session


async def main() -> None:
    """Initialize and start the bot."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    
    # Initialize the database
    await init_db()
    logger.info("Database initialized")
    
    # Create the bot instance with DefaultBotProperties
    bot = Bot(
        token=settings.telegram.token, 
        default=DefaultBotProperties(parse_mode="HTML")
    )
    
    # Select storage (memory for development, redis for production)
    if settings.database.url.startswith("sqlite"):
        storage = MemoryStorage()
        logger.info("Using memory storage for FSM")
    else:
        # For production, you would use Redis
        # storage = RedisStorage.from_url("redis://localhost:6379/0")
        storage = MemoryStorage()  # Fallback to memory for now
        logger.info("Using memory storage for FSM (production)")
    
    # Create the dispatcher
    dp = Dispatcher(storage=storage)
    
    # Register all routers
    dp.include_router(commands.router)
    dp.include_router(quiz.router)
    dp.include_router(report.router)
    
    # Add session middleware with our custom context manager
    dp.workflow_data.update(
        session_pool=session_pool,
    )
    
    try:
        # Start polling
        logger.info("Starting bot polling...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Close the database connection
        await close_db()
        logger.info("Database connection closed")


if __name__ == "__main__":
    try:
        # Run the main function
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Log exit
        logger.info("Bot stopped")
    except Exception as e:
        # Log unexpected exceptions
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1) 