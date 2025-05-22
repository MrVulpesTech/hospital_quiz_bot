"""
User model for the Hospital Quiz Bot.
This module provides the User model for storing Telegram user information.
"""

from typing import Optional

from sqlalchemy import Column, String, Integer, Boolean

from .base import BaseModel


class User(BaseModel):
    """User model for storing Telegram user information."""
    
    __tablename__ = "users"
    
    # Telegram user ID
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    
    # User information
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    
    # User settings
    is_admin = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    
    # User preferences
    language = Column(String, nullable=True)  # 'uk' for Ukrainian, 'de' for German
    
    def __repr__(self) -> str:
        """Return a string representation of the User."""
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"
    
    @property
    def full_name(self) -> str:
        """Return the full name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.username:
            return self.username
        else:
            return f"User {self.telegram_id}"
    
    @classmethod
    def from_telegram_user(cls, telegram_user):
        """Create a User from a Telegram user object."""
        return cls(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            language_code=telegram_user.language_code,
        ) 