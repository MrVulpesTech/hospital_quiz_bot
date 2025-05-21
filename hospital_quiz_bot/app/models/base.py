"""
Base database model for the Hospital Quiz Bot.
This module provides the base model for all database entities.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Create the base model
Base = declarative_base()


class BaseModel(Base):
    """Base model for all database entities with common fields."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        """Create a model instance from a dictionary."""
        return cls(**{
            k: v for k, v in data.items() 
            if k in [column.name for column in cls.__table__.columns]
        }) 