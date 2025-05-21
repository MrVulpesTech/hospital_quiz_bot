"""
Report service for the Hospital Quiz Bot.
This module provides functionality for generating medical reports from quiz responses.
"""

from typing import Dict, Any, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from hospital_quiz_bot.app.models.quiz_response import QuizResponse
from hospital_quiz_bot.app.database.repository import QuizResponseRepository
from hospital_quiz_bot.app.services.openai_service import OpenAIService
from hospital_quiz_bot.app.services.quiz_service import QuizService
from hospital_quiz_bot.config.logging_config import logger


class ReportService:
    """Service for generating reports from quiz responses."""
    
    def __init__(self, session: AsyncSession):
        """Initialize the report service."""
        self.session = session
        self.quiz_response_repo = QuizResponseRepository(session)
        self.openai_service = OpenAIService()
        self.quiz_service = QuizService()
    
    async def generate_report_from_session(self, session_id: str) -> Optional[str]:
        """Generate a report from a quiz session."""
        quiz_response = await self.quiz_response_repo.get_by_session_id(session_id)
        if not quiz_response:
            logger.error(f"Quiz session not found: {session_id}")
            return None
            
        return await self.generate_report(quiz_response)
    
    async def generate_report(self, quiz_response: QuizResponse) -> Optional[str]:
        """Generate a report from a quiz response."""
        if not quiz_response.is_complete:
            logger.warning(f"Quiz is not complete: {quiz_response.id}")
            return None
            
        try:
            # Format the responses for the prompt
            formatted_responses = self._format_responses_for_prompt(quiz_response)
            
            # Generate the report - use synchronous method
            # Important: Don't use the async/await pattern here since we've made the OpenAI call synchronous
            report = self.openai_service.generate_report(formatted_responses)
            
            if report:
                # Save the report
                quiz_response.report = report
                await self.quiz_response_repo.update(quiz_response)
                await self.quiz_response_repo.commit()
                
                logger.info(f"Generated report for quiz: {quiz_response.id}")
                
            return report
        except Exception as e:
            logger.error(f"Error in generate_report: {str(e)}")
            return f"Помилка генерації звіту: {str(e)}"
    
    def _format_responses_for_prompt(self, quiz_response: QuizResponse) -> str:
        """Format the responses for the OpenAI prompt."""
        formatted_lines = []
        responses = quiz_response.get_all_responses()
        
        # Map question IDs to their actual text
        for question_id, answer in responses.items():
            question = self.quiz_service.get_question_by_id(question_id)
            if question:
                question_text = question["text"]
                
                # Special case formatting for certain question types
                if question["type"] == "text_input" and question.get("placeholder"):
                    # For questions with expected format
                    if not answer:
                        answer = "Не вказано"
                        
                formatted_lines.append(f"{question_text}: {answer}")
        
        return "\n".join(formatted_lines)
    
    async def get_report(self, session_id: str) -> Optional[str]:
        """Get a report for a quiz session."""
        quiz_response = await self.quiz_response_repo.get_by_session_id(session_id)
        if not quiz_response:
            logger.error(f"Quiz session not found: {session_id}")
            return None
            
        # If the report exists, return it
        if quiz_response.report:
            return quiz_response.report
            
        # Otherwise, generate it
        return await self.generate_report(quiz_response)
    
    async def get_reports_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all reports for a user."""
        quiz_responses = await self.quiz_response_repo.get_completed_quizzes_for_user(user_id)
        
        reports = []
        for quiz_response in quiz_responses:
            if quiz_response.report:
                reports.append({
                    "id": quiz_response.id,
                    "session_id": quiz_response.session_id,
                    "created_at": quiz_response.created_at,
                    "report": quiz_response.report,
                })
                
        return reports 