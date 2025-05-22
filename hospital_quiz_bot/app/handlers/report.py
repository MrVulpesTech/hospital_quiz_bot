"""
Report handlers for the Hospital Quiz Bot.
This module provides handlers for viewing and managing reports.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from hospital_quiz_bot.app.database.repository import UserRepository, QuizResponseRepository
from hospital_quiz_bot.app.services.report_service import ReportService
from hospital_quiz_bot.app.utils.formatters import format_reports_list_message, format_report_message
from hospital_quiz_bot.app.keyboards.reply import get_main_keyboard
from hospital_quiz_bot.app.keyboards.inline import get_reports_keyboard, get_report_actions_keyboard
from hospital_quiz_bot.app.states.quiz_states import ReportStates
from hospital_quiz_bot.app.handlers.quiz import cmd_quiz
from hospital_quiz_bot.config.logging_config import logger

# Create a router for report handlers
router = Router()


@router.message(Command("reports"))
async def cmd_reports(message: Message, state: FSMContext, session_pool):
    """Handle the /reports command."""
    # Clear any previous state
    await state.clear()
    
    # Get user's language preference
    language = "uk"  # Default to Ukrainian
    
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        if user and user.language:
            language = user.language
    
    # Get the user's reports
    async with session_pool() as session:
        user_repo = UserRepository(session)
        report_service = ReportService(session, language=language)
        
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        if not user:
            user = await user_repo.get_or_create_user(message.from_user)
        
        reports = await report_service.get_reports_for_user(user.id)
    
    # Format the message based on whether there are reports
    formatted_message = format_reports_list_message(len(reports), language)
    
    # Set the state to listing
    await state.set_state(ReportStates.listing)
    
    # Store the reports in the state
    await state.update_data(reports=reports)
    
    if not reports:
        # If no reports, just show the main keyboard
        await message.answer(
            formatted_message,
            reply_markup=get_main_keyboard(language),
        )
    else:
        # If there are reports, show the reports keyboard
        await message.answer(
            formatted_message,
            reply_markup=get_reports_keyboard(reports, language),
        )
    
    logger.info(f"User {message.from_user.id} requested reports list")


@router.callback_query(F.data.startswith("report:"))
async def view_report(callback: CallbackQuery, state: FSMContext, session_pool):
    """Handle viewing a specific report."""
    # Extract the session ID from the callback data
    session_id = callback.data.split(":", 1)[1]
    
    # Get user's language preference
    language = "uk"  # Default to Ukrainian
    
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(callback.from_user.id)
        if user and user.language:
            language = user.language
    
    # Get the report
    async with session_pool() as session:
        report_service = ReportService(session, language=language)
        report = await report_service.get_report(session_id)
    
    if not report:
        error_message = "Помилка: Звіт не знайдено. Будь ласка, спробуйте ще раз."
        if language == "de":
            error_message = "Fehler: Bericht nicht gefunden. Bitte versuchen Sie es erneut."
            
        await callback.message.answer(
            error_message,
            reply_markup=get_main_keyboard(language),
        )
        await callback.answer()
        await state.clear()
        return
    
    # Set the state to viewing
    await state.set_state(ReportStates.viewing)
    
    # Store the session ID in the state
    await state.update_data(
        session_id=session_id,
    )
    
    # Format and send the report
    formatted_report = format_report_message(report, language)
    
    if isinstance(formatted_report, list):
        # If the report is split into multiple messages
        for part in formatted_report:
            await callback.message.answer(part)
    else:
        # If the report is a single message
        await callback.message.answer(formatted_report)
    
    # Send the actions keyboard
    report_actions_message = "Що ви хочете зробити зі звітом?"
    if language == "de":
        report_actions_message = "Was möchten Sie mit dem Bericht tun?"
        
    await callback.message.answer(
        report_actions_message,
        reply_markup=get_report_actions_keyboard(language),
    )
    
    # Answer the callback
    await callback.answer()
    
    logger.info(f"User {callback.from_user.id} viewed report with session ID {session_id}")


@router.callback_query(F.data.startswith("reports_page:"))
async def paginate_reports(callback: CallbackQuery, state: FSMContext):
    """Handle pagination for reports list."""
    # Extract the page number from the callback data
    page = int(callback.data.split(":", 1)[1])
    
    # Get the reports from the state
    data = await state.get_data()
    reports = data.get("reports", [])
    
    if not reports:
        await callback.message.answer(
            "Немає доступних звітів.",
            reply_markup=get_main_keyboard(),
        )
        await callback.answer()
        await state.clear()
        return
    
    # Update the reports keyboard with the new page
    await callback.message.edit_reply_markup(
        reply_markup=get_reports_keyboard(reports, page=page),
    )
    
    # Answer the callback
    await callback.answer()


@router.callback_query(F.data == "back")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    """Handle going back to the main menu."""
    # Clear the state
    await state.clear()
    
    # Send the main keyboard
    await callback.message.answer(
        "Головне меню",
        reply_markup=get_main_keyboard(),
    )
    
    # Answer the callback
    await callback.answer()


@router.callback_query(F.data == "reports")
async def back_to_reports(callback: CallbackQuery, state: FSMContext, session_pool):
    """Handle going back to the reports list."""
    # Clear the state
    await state.clear()
    
    # Redirect to the reports command
    await cmd_reports(callback.message, state, session_pool)
    
    # Answer the callback
    await callback.answer()


@router.callback_query(F.data == "new_quiz")
async def start_new_quiz(callback: CallbackQuery, state: FSMContext, session_pool):
    """Handle starting a new quiz from report view."""
    # Clear the state
    await state.clear()
    
    # Use the cmd_quiz handler directly to start a new quiz
    await cmd_quiz(callback.message, state, session_pool)
    
    # Answer the callback
    await callback.answer()


@router.message(F.text == "/quiz")
async def handle_quiz_command(message: Message, state: FSMContext, session_pool):
    """Handle the /quiz command as a message."""
    # Clear the state
    await state.clear()
    
    # Redirect to the quiz command handler
    await cmd_quiz(message, state, session_pool)


# Comment out the share_report handler since we're not using it now
# @router.callback_query(F.data.startswith("share:"))
# async def share_report(callback: CallbackQuery, state: FSMContext, session_pool):
#     """Handle sharing a report."""
#     # Extract the session ID from the callback data
#     session_id = callback.data.split(":", 1)[1]
#     
#     # Get the report
#     async with session_pool() as session:
#         report_service = ReportService(session)
#         report = await report_service.get_report(session_id)
#     
#     if not report:
#         await callback.message.answer(
#             "Помилка: Звіт не знайдено. Будь ласка, спробуйте ще раз.",
#             reply_markup=get_main_keyboard(),
#         )
#         await callback.answer()
#         await state.clear()
#         return
#     
#     # For now, just provide instructions on how to share
#     await callback.message.answer(
#         "Щоб поділитися звітом, ви можете скопіювати його та надіслати безпосередньо у повідомленні."
#     )
#     
#     # Answer the callback
#     await callback.answer()
#     
#     logger.info(f"User {callback.from_user.id} requested to share report {session_id}") 