"""
Quiz response model for the Hospital Quiz Bot.
This module provides the QuizResponse model for storing user quiz responses.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class QuizResponse(BaseModel):
    """QuizResponse model for storing user quiz responses."""
    
    __tablename__ = "quiz_responses"
    
    # User who provided the responses
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", backref="quiz_responses")
    
    # Quiz responses
    responses = Column(JSON, nullable=False, default=dict)
    
    # Report generation status
    is_complete = Column(Boolean, default=False, nullable=False)
    report = Column(Text, nullable=True)
    
    # Session information
    session_id = Column(String, nullable=False, index=True)
    
    def __repr__(self) -> str:
        """Return a string representation of the QuizResponse."""
        return f"<QuizResponse(id={self.id}, user_id={self.user_id}, is_complete={self.is_complete})>"
    
    def get_response(self, question_id: str) -> Optional[str]:
        """Get a response for a specific question."""
        if isinstance(self.responses, str):
            responses = json.loads(self.responses)
        else:
            responses = self.responses
            
        return responses.get(question_id)
    
    def set_response(self, question_id: str, answer: str) -> None:
        """Set a response for a specific question."""
        if isinstance(self.responses, str):
            responses = json.loads(self.responses)
        else:
            responses = dict(self.responses) if self.responses else {}
            
        responses[question_id] = answer
        self.responses = responses
    
    def get_all_responses(self) -> Dict[str, str]:
        """Get all responses as a dictionary."""
        if isinstance(self.responses, str):
            return json.loads(self.responses)
        return dict(self.responses) if self.responses else {}
    
    def format_for_prompt(self) -> str:
        """Format the responses for use in the OpenAI prompt."""
        formatted_responses = []
        for question_id, answer in self.get_all_responses().items():
            # Convert question_id to a human-readable form
            # This assumes question_ids match the data in quizes.yaml
            # In a real implementation, we would map these to actual question text
            formatted_question = question_id.replace("_", " ").capitalize()
            formatted_responses.append(f"{formatted_question}: {answer}")
            
        return "\n".join(formatted_responses)
    
    def is_ready_for_report(self) -> bool:
        """Check if all required questions have been answered."""
        # In a real implementation, we would check against the required questions
        # For now, assume the quiz is complete if it's marked as complete
        return self.is_complete and not self.report
    
    def set_completed(self) -> None:
        """Mark the quiz as completed."""
        self.is_complete = True 