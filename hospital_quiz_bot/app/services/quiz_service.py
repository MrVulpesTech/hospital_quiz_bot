"""
Quiz service for the Hospital Quiz Bot.
This module provides functionality for loading and managing quiz questions.
"""

import uuid
from typing import Dict, List, Optional, Any, Union

import yaml

from hospital_quiz_bot.config.settings import settings
from hospital_quiz_bot.config.logging_config import logger


class QuizService:
    """Service for loading and managing quiz questions."""
    
    # Singleton instance
    _instance = None
    _initialized = False
    
    def __new__(cls, quiz_file=None):
        """Create a new QuizService instance or return the existing one."""
        if cls._instance is None:
            cls._instance = super(QuizService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, quiz_file=None):
        """Initialize the quiz service with the quiz file path."""
        # Only initialize once
        if not QuizService._initialized:
            self.quiz_file = quiz_file or settings.quiz_file
            self.questions = []
            self.questions_by_id = {}
            self._load_questions()
            QuizService._initialized = True
    
    def _load_questions(self) -> None:
        """Load questions from the quiz file."""
        try:
            with open(self.quiz_file, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                
            if not data or "questions" not in data:
                logger.error(f"Invalid quiz file format: {self.quiz_file}")
                return
                
            self.questions = data["questions"]
            self.questions_by_id = {q["id"]: q for q in self.questions}
            logger.info(f"Loaded {len(self.questions)} questions from {self.quiz_file}")
        except Exception as e:
            logger.error(f"Error loading quiz file: {str(e)}")
            self.questions = []
            self.questions_by_id = {}
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """Get all questions."""
        return self.questions
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Get a question by its ID."""
        return self.questions_by_id.get(question_id)
    
    def get_question_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """Get a question by its index."""
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
    
    def get_question_index(self, question_id: str) -> Optional[int]:
        """Get the index of a question by its ID."""
        for i, question in enumerate(self.questions):
            if question["id"] == question_id:
                return i
        return None
    
    def get_question_options(self, question_id: str) -> List[str]:
        """Get the options for a question."""
        question = self.get_question_by_id(question_id)
        if question and "options" in question:
            return question["options"]
        return []
    
    def get_total_questions(self) -> int:
        """Get the total number of questions."""
        return len(self.questions)
    
    def is_valid_answer(self, question_id: str, answer: str) -> bool:
        """Check if an answer is valid for a question."""
        question = self.get_question_by_id(question_id)
        if not question:
            return False
            
        if question["type"] == "single_choice":
            return answer in question["options"]
        elif question["type"] == "text_input":
            # Text input validation could be more complex
            return bool(answer.strip())
        elif question["type"] == "optional_text":
            if answer in question["options"]:
                return True
            # If the answer is not an option, it might be follow-up text
            return bool(answer.strip())
        
        return False
    
    def create_new_session(self) -> str:
        """Create a new quiz session."""
        return str(uuid.uuid4())
    
    def format_question_text(self, question: Dict[str, Any]) -> str:
        """Format the question text for display."""
        if question["type"] == "text_input" and "placeholder" in question:
            return f"{question['text']}\n(Формат: {question['placeholder']})"
        return question["text"] 