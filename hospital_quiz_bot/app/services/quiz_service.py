"""
Quiz service for the Hospital Quiz Bot.
This module provides functionality for loading and managing quiz questions.
"""

import os
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
    _language_quiz_files = {
        "uk": settings.quiz_file,  # Default Ukrainian file
        "de": str(settings.quiz_file).replace("quizes.yaml", "quizes_de.yaml")  # German file
    }
    _loaded_questions = {}
    
    def __new__(cls, language=None):
        """Create a new QuizService instance or return the existing one."""
        if cls._instance is None:
            cls._instance = super(QuizService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, language=None):
        """Initialize the quiz service with the quiz file path."""
        # Only initialize once
        if not QuizService._initialized:
            self._load_all_languages()
            QuizService._initialized = True
        
        # Set the active language
        self.language = language or "uk"  # Default to Ukrainian
        self.questions = self._loaded_questions.get(self.language, [])
        self.questions_by_id = {q["id"]: q for q in self.questions}
    
    def _load_all_languages(self) -> None:
        """Load questions for all supported languages."""
        for lang, file_path in self._language_quiz_files.items():
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                    
                if not data or "questions" not in data:
                    logger.error(f"Invalid quiz file format: {file_path}")
                    continue
                    
                self._loaded_questions[lang] = data["questions"]
                logger.info(f"Loaded {len(data['questions'])} questions for language {lang} from {file_path}")
            except Exception as e:
                logger.error(f"Error loading quiz file for language {lang}: {str(e)}")
                self._loaded_questions[lang] = []
    
    def set_language(self, language: str) -> None:
        """Set the active language for the quiz service."""
        if language in self._language_quiz_files:
            self.language = language
            self.questions = self._loaded_questions.get(language, [])
            self.questions_by_id = {q["id"]: q for q in self.questions}
            logger.info(f"Set active language to: {language}")
        else:
            logger.error(f"Language not supported: {language}")
    
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