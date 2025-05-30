"""
Quiz handlers for the Hospital Quiz Bot.
This module provides handlers for the quiz conversation flow.
"""

import uuid
from typing import Dict, Any, Optional, Union, List

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from hospital_quiz_bot.app.database.repository import UserRepository, QuizResponseRepository
from hospital_quiz_bot.app.models.quiz_response import QuizResponse
from hospital_quiz_bot.app.services.quiz_service import QuizService
from hospital_quiz_bot.app.services.report_service import ReportService
from hospital_quiz_bot.app.utils.formatters import (
    format_quiz_start_message,
    format_question,
    format_quiz_confirmation_message,
    format_report_generation_message,
    format_report_message,
)
from hospital_quiz_bot.app.keyboards.reply import (
    get_quiz_options_keyboard,
    get_confirmation_keyboard,
    get_cancel_keyboard,
    get_report_actions_keyboard,
    get_main_keyboard,
)
from hospital_quiz_bot.app.states.quiz_states import QuizStates
from hospital_quiz_bot.config.logging_config import logger

# Create a router for quiz handlers
router = Router()


@router.message(Command("quiz"))
async def cmd_quiz(message: Message, state: FSMContext, session_pool):
    """Handle the /quiz command."""
    # Get user's language preference
    language = "uk"  # Default to Ukrainian
    
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        if user and user.language:
            language = user.language
    
    # Create a new quiz session
    quiz_service = QuizService(language)
    quiz_service.set_language(language)
    session_id = quiz_service.create_new_session()
    
    # Store the session ID in FSM state
    await state.update_data(
        session_id=session_id,
        current_question_index=0,
        current_question_id=quiz_service.get_question_by_index(0)["id"],
        language=language,  # Store the language preference
    )
    
    # Create a new quiz response record
    async with session_pool() as session:
        quiz_repo = QuizResponseRepository(session)
        
        # Create a new quiz response
        quiz_response = await quiz_repo.create_new(
            user_id=message.from_user.id,
            session_id=session_id,
            language=language,  # Set the language for the quiz response
        )
        
        if not quiz_response:
            # Handle error
            error_message = "Помилка: Не вдалося створити нове опитування. Спробуйте ще раз."
            if language == "de":
                error_message = "Fehler: Konnte keine neue Umfrage erstellen. Bitte versuchen Sie es erneut."
                
            await message.answer(
                error_message,
                reply_markup=get_main_keyboard(language),
            )
            return
        
        await quiz_repo.commit()
    
    # Move to the answering state
    await state.set_state(QuizStates.answering)
    
    # Get the first question
    first_question = quiz_service.get_question_by_index(0)
    question_text = quiz_service.format_question_text(first_question)
    
    formatted_question = format_question(
        question_text,
        0,
        quiz_service.get_total_questions(),
        language,
    )
    
    # Send the first question with appropriate keyboard
    if first_question["type"] in ["single_choice", "optional_text"]:
        # For questions with options
        options = first_question["options"]
        await message.answer(
            formatted_question,
            reply_markup=get_quiz_options_keyboard(options, language),
        )
    else:
        # For text input questions
        await message.answer(
            formatted_question,
            reply_markup=get_cancel_keyboard(language),
        )
    
    logger.info(f"User {message.from_user.id} started a new quiz with session ID {session_id} in language {language}")


@router.message(QuizStates.answering, F.text)
async def process_answer(message: Message, state: FSMContext, session_pool):
    """Process an answer to a quiz question."""
    # Get the state data
    data = await state.get_data()
    session_id = data.get("session_id")
    current_question_index = data.get("current_question_index", 0)
    current_question_id = data.get("current_question_id")
    language = data.get("language", "uk")  # Get the language from state
    
    # Initialize quiz service with language
    quiz_service = QuizService(language)
    # Ensure the language is set
    quiz_service.set_language(language)
    
    # Get the current question
    current_question = quiz_service.get_question_by_id(current_question_id)
    
    # Check if the answer is valid
    if not quiz_service.is_valid_answer(current_question_id, message.text):
        # Special case for navigation commands
        if message.text == "⬅️ Назад" or message.text == "⬅️ Zurück":
            # Go back to the previous question
            if current_question_index > 0:
                new_index = current_question_index - 1
                new_question = quiz_service.get_question_by_index(new_index)
                
                await state.update_data(
                    current_question_index=new_index,
                    current_question_id=new_question["id"],
                )
                
                # Send the previous question
                question_text = quiz_service.format_question_text(new_question)
                formatted_question = format_question(
                    question_text,
                    new_index,
                    quiz_service.get_total_questions(),
                    language,
                )
                
                if new_question["type"] in ["single_choice", "optional_text"]:
                    # For questions with options
                    options = new_question["options"]
                    await message.answer(
                        formatted_question,
                        reply_markup=get_quiz_options_keyboard(options, language),
                    )
                else:
                    # For text input questions
                    await message.answer(
                        formatted_question,
                        reply_markup=get_cancel_keyboard(language),
                    )
                
                return
            else:
                # If we're at the first question, inform the user
                first_question_message = "Це перше питання. Неможливо повернутися назад."
                if language == "de":
                    first_question_message = "Dies ist die erste Frage. Es ist nicht möglich, zurückzugehen."
                
                await message.answer(first_question_message)
                return
        
        # If the answer is not valid and not a navigation command
        invalid_answer_message = "Будь ласка, виберіть або введіть правильну відповідь для цього питання."
        if language == "de":
            invalid_answer_message = "Bitte wählen Sie oder geben Sie eine gültige Antwort für diese Frage ein."
            
        await message.answer(invalid_answer_message)
        return
    
    # Store the answer
    async with session_pool() as session:
        quiz_repo = QuizResponseRepository(session)
        
        quiz_response = await quiz_repo.get_by_session_id(session_id)
        if not quiz_response:
            logger.error(f"Quiz session not found: {session_id}")
            
            error_message = "Помилка: Сесію опитування не знайдено. Будь ласка, почніть опитування знову."
            if language == "de":
                error_message = "Fehler: Sitzung nicht gefunden. Bitte starten Sie die Umfrage erneut."
                
            await message.answer(
                error_message,
                reply_markup=get_main_keyboard(language),
            )
            await state.clear()
            return
        
        quiz_response.set_response(current_question_id, message.text)
        await quiz_repo.update(quiz_response)
        await quiz_repo.commit()
    
    # Check for special case of optional_text
    if current_question["type"] == "optional_text" and (message.text == "Так" or message.text == "Ja"):
        # We need to collect additional text input
        await state.update_data(
            awaiting_follow_up=True,
        )
        
        await state.set_state(QuizStates.text_input)
        
        follow_up_text = current_question.get("follow_up_text", "Введіть додаткову інформацію:")
        if language == "de" and not follow_up_text.startswith("Geben Sie"):
            follow_up_text = "Geben Sie zusätzliche Informationen ein:"
            
        await message.answer(
            follow_up_text,
            reply_markup=get_cancel_keyboard(language),
        )
        return
    
    # Move to the next question or confirmation
    next_index = current_question_index + 1
    
    if next_index < quiz_service.get_total_questions():
        # There are more questions
        next_question = quiz_service.get_question_by_index(next_index)
        
        await state.update_data(
            current_question_index=next_index,
            current_question_id=next_question["id"],
        )
        
        # Send the next question
        question_text = quiz_service.format_question_text(next_question)
        formatted_question = format_question(
            question_text,
            next_index,
            quiz_service.get_total_questions(),
            language,
        )
        
        if next_question["type"] in ["single_choice", "optional_text"]:
            # For questions with options
            options = next_question["options"]
            await message.answer(
                formatted_question,
                reply_markup=get_quiz_options_keyboard(options, language),
            )
        else:
            # For text input questions
            await message.answer(
                formatted_question,
                reply_markup=get_cancel_keyboard(language),
            )
    else:
        # No more questions, move to confirmation
        await state.set_state(QuizStates.confirmation)
        
        # Get all responses
        async with session_pool() as session:
            quiz_repo = QuizResponseRepository(session)
            quiz_response = await quiz_repo.get_by_session_id(session_id)
            responses = quiz_response.get_all_responses()
        
        # Format the confirmation message
        confirmation_message = format_quiz_confirmation_message(
            responses,
            quiz_service.get_all_questions(),
            language,
        )
        
        await message.answer(
            confirmation_message,
            reply_markup=get_confirmation_keyboard(language),
        )


@router.message(QuizStates.text_input, F.text)
async def process_text_input(message: Message, state: FSMContext, session_pool):
    """Process text input for an optional_text question."""
    # Get the state data
    data = await state.get_data()
    session_id = data.get("session_id")
    current_question_id = data.get("current_question_id")
    awaiting_follow_up = data.get("awaiting_follow_up", False)
    language = data.get("language", "uk")  # Get language from state
    
    if not awaiting_follow_up:
        # If we're not awaiting follow-up, this is unexpected
        error_message = "Помилка: Несподіваний стан. Будь ласка, почніть опитування знову."
        if language == "de":
            error_message = "Fehler: Unerwarteter Zustand. Bitte starten Sie die Umfrage erneut."
            
        await message.answer(
            error_message,
            reply_markup=get_main_keyboard(language),
        )
        await state.clear()
        return
    
    # Store the additional text
    async with session_pool() as session:
        quiz_repo = QuizResponseRepository(session)
        
        quiz_response = await quiz_repo.get_by_session_id(session_id)
        if not quiz_response:
            logger.error(f"Quiz session not found: {session_id}")
            
            error_message = "Помилка: Сесію опитування не знайдено. Будь ласка, почніть опитування знову."
            if language == "de":
                error_message = "Fehler: Sitzung nicht gefunden. Bitte starten Sie die Umfrage erneut."
                
            await message.answer(
                error_message,
                reply_markup=get_main_keyboard(language),
            )
            await state.clear()
            return
        
        # Update the response with the additional text
        quiz_response.set_response(current_question_id, message.text)
        await quiz_repo.update(quiz_response)
        await quiz_repo.commit()
    
    # Reset the awaiting_follow_up flag
    await state.update_data(
        awaiting_follow_up=False,
    )
    
    # Continue to the next question
    await state.set_state(QuizStates.answering)
    
    # Initialize quiz service with language
    quiz_service = QuizService(language)
    quiz_service.set_language(language)
    
    # Get the current index and move to the next question
    current_question_index = data.get("current_question_index", 0)
    next_index = current_question_index + 1
    
    if next_index < quiz_service.get_total_questions():
        # There are more questions
        next_question = quiz_service.get_question_by_index(next_index)
        
        await state.update_data(
            current_question_index=next_index,
            current_question_id=next_question["id"],
        )
        
        # Send the next question
        question_text = quiz_service.format_question_text(next_question)
        formatted_question = format_question(
            question_text,
            next_index,
            quiz_service.get_total_questions(),
            language,
        )
        
        if next_question["type"] in ["single_choice", "optional_text"]:
            # For questions with options
            options = next_question["options"]
            await message.answer(
                formatted_question,
                reply_markup=get_quiz_options_keyboard(options, language),
            )
        else:
            # For text input questions
            await message.answer(
                formatted_question,
                reply_markup=get_cancel_keyboard(language),
            )
    else:
        # No more questions, move to confirmation
        await state.set_state(QuizStates.confirmation)
        
        # Get all responses
        async with session_pool() as session:
            quiz_repo = QuizResponseRepository(session)
            quiz_response = await quiz_repo.get_by_session_id(session_id)
            responses = quiz_response.get_all_responses()
        
        # Format the confirmation message
        confirmation_message = format_quiz_confirmation_message(
            responses,
            quiz_service.get_all_questions(),
            language,
        )
        
        await message.answer(
            confirmation_message,
            reply_markup=get_confirmation_keyboard(language),
        )


@router.message(QuizStates.confirmation, F.text.in_(["✅ Так, завершити", "✅ Ja, abschließen"]))
async def confirm_quiz(message: Message, state: FSMContext, session_pool):
    """Handle quiz confirmation and generate report."""
    # Get the state data
    data = await state.get_data()
    session_id = data.get("session_id")
    language = data.get("language", "uk")
    
    # Mark the quiz as complete
    async with session_pool() as session:
        quiz_repo = QuizResponseRepository(session)
        
        quiz_response = await quiz_repo.get_by_session_id(session_id)
        if not quiz_response:
            logger.error(f"Quiz session not found: {session_id}")
            
            error_message = "Помилка: Сесію опитування не знайдено. Будь ласка, почніть опитування знову."
            if language == "de":
                error_message = "Fehler: Sitzung nicht gefunden. Bitte starten Sie die Umfrage erneut."
                
            await message.answer(
                error_message,
                reply_markup=get_main_keyboard(language),
            )
            await state.clear()
            return
        
        quiz_response.set_completed()
        await quiz_repo.update(quiz_response)
        await quiz_repo.commit()
    
    # Move to the report generation state
    await state.set_state(QuizStates.generating_report)
    
    # Send the generating message
    await message.answer(
        format_report_generation_message(language),
        reply_markup=get_cancel_keyboard(language),
    )
    
    # Generate the report
    async with session_pool() as session:
        report_service = ReportService(session, language=language)
        report = await report_service.generate_report_from_session(session_id)
    
    if not report:
        logger.error(f"Failed to generate report for session: {session_id}")
        
        error_message = "Помилка: Не вдалося згенерувати звіт. Будь ласка, спробуйте ще раз."
        if language == "de":
            error_message = "Fehler: Bericht konnte nicht erstellt werden. Bitte versuchen Sie es erneut."
            
        await message.answer(
            error_message,
            reply_markup=get_main_keyboard(language),
        )
        await state.clear()
        return
    
    # Move to the report viewing state
    await state.set_state(QuizStates.viewing_report)
    
    # Format and send the report
    formatted_report = format_report_message(report, language)
    
    if isinstance(formatted_report, list):
        # If the report is split into multiple messages
        for part in formatted_report:
            await message.answer(part)
    else:
        # If the report is a single message
        await message.answer(formatted_report)
    
    # Send the actions keyboard
    report_actions_message = "Що ви хочете зробити зі звітом?"
    if language == "de":
        report_actions_message = "Was möchten Sie mit dem Bericht tun?"
        
    await message.answer(
        report_actions_message,
        reply_markup=get_report_actions_keyboard(language),
    )
    
    logger.info(f"Generated report for user {message.from_user.id}, session {session_id}")


@router.message(QuizStates.confirmation, F.text.in_(["⬅️ Повернутися до питань", "⬅️ Zurück zu den Fragen"]))
async def return_to_questions(message: Message, state: FSMContext):
    """Handle returning to questions from confirmation."""
    # Get the state data
    data = await state.get_data()
    language = data.get("language", "uk")
    
    # Go back to the answering state
    await state.set_state(QuizStates.answering)
    
    # Go back to the last question
    quiz_service = QuizService(language)
    quiz_service.set_language(language)
    
    last_index = quiz_service.get_total_questions() - 1
    last_question = quiz_service.get_question_by_index(last_index)
    
    await state.update_data(
        current_question_index=last_index,
        current_question_id=last_question["id"],
    )
    
    # Send the last question again
    question_text = quiz_service.format_question_text(last_question)
    formatted_question = format_question(
        question_text,
        last_index,
        quiz_service.get_total_questions(),
        language,
    )
    
    if last_question["type"] in ["single_choice", "optional_text"]:
        # For questions with options
        options = last_question["options"]
        await message.answer(
            formatted_question,
            reply_markup=get_quiz_options_keyboard(options, language),
        )
    else:
        # For text input questions
        await message.answer(
            formatted_question,
            reply_markup=get_cancel_keyboard(language),
        )
    
    logger.info(f"User {message.from_user.id} returned to questions from confirmation") 