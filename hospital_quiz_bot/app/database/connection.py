"""
Database connection for the Hospital Quiz Bot.
This module provides the database connection and session factory.
"""

import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from hospital_quiz_bot.config.settings import settings
from hospital_quiz_bot.app.models.base import Base

# Create the async engine
engine = create_async_engine(
    settings.database.url.replace("sqlite:///", "sqlite+aiosqlite:///"),
    echo=settings.database.echo,
)

# Create the session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close the database connection."""
    await engine.dispose() 