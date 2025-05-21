"""
Repository module for the Hospital Quiz Bot.
This module provides repository classes for data access patterns.
"""

from typing import List, Optional, TypeVar, Generic, Type, Any, Dict

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from hospital_quiz_bot.app.models.base import BaseModel
from hospital_quiz_bot.app.models.user import User
from hospital_quiz_bot.app.models.quiz_response import QuizResponse

# Generic type for model classes
T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    """Base repository class for data access patterns."""
    
    def __init__(self, session: AsyncSession, model_class: Type[T]):
        self.session = session
        self.model_class = model_class
    
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get an entity by its ID."""
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[T]:
        """Get all entities."""
        stmt = select(self.model_class)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def add(self, entity: T) -> T:
        """Add a new entity."""
        self.session.add(entity)
        await self.session.flush()
        return entity
    
    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        self.session.add(entity)
        await self.session.flush()
        return entity
    
    async def delete(self, entity: T) -> None:
        """Delete an entity."""
        await self.session.delete(entity)
        await self.session.flush()
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()
    
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.session.rollback()


class UserRepository(BaseRepository[User]):
    """Repository for User entities."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get a user by their Telegram ID."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_or_create_user(self, telegram_user) -> User:
        """Get a user by their Telegram ID or create a new one."""
        user = await self.get_by_telegram_id(telegram_user.id)
        if not user:
            user = User.from_telegram_user(telegram_user)
            await self.add(user)
            await self.commit()
        return user


class QuizResponseRepository(BaseRepository[QuizResponse]):
    """Repository for QuizResponse entities."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, QuizResponse)
    
    async def get_by_session_id(self, session_id: str) -> Optional[QuizResponse]:
        """Get a quiz response by its session ID."""
        stmt = select(QuizResponse).where(QuizResponse.session_id == session_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> List[QuizResponse]:
        """Get all quiz responses for a user."""
        stmt = select(QuizResponse).where(
            QuizResponse.user_id == user_id
        ).order_by(QuizResponse.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_active_quiz_for_user(self, user_id: int) -> Optional[QuizResponse]:
        """Get the active (incomplete) quiz for a user."""
        stmt = select(QuizResponse).where(
            QuizResponse.user_id == user_id,
            QuizResponse.is_complete == False
        ).order_by(QuizResponse.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_completed_quizzes_for_user(self, user_id: int) -> List[QuizResponse]:
        """Get all completed quizzes for a user."""
        stmt = select(QuizResponse).where(
            QuizResponse.user_id == user_id,
            QuizResponse.is_complete == True
        ).order_by(QuizResponse.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all()) 