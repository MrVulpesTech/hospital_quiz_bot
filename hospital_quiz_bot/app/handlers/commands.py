"""
Command handlers for the Hospital Quiz Bot.
This module provides handlers for basic bot commands.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from hospital_quiz_bot.app.database.repository import UserRepository
from hospital_quiz_bot.app.utils.formatters import format_welcome_message, format_help_message
from hospital_quiz_bot.app.keyboards.reply import get_main_keyboard, remove_keyboard, get_language_keyboard
from hospital_quiz_bot.app.states.quiz_states import UserStates
from hospital_quiz_bot.config.logging_config import logger

# Create a router for command handlers
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session_pool, state: FSMContext):
    """Handle the /start command."""
    # Create a session and get/create the user
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create_user(message.from_user)
    
    # Check if the user has a language set
    if not user.language:
        # Ask for language selection
        await message.answer(
            "Please select your preferred language / Будь ласка, виберіть мову / Bitte wählen Sie Ihre bevorzugte Sprache:",
            reply_markup=get_language_keyboard()
        )
        await state.set_state(UserStates.selecting_language)
    else:
        # Send welcome message with existing language
        await message.answer(
            format_welcome_message(user.full_name, user.language),
            reply_markup=get_main_keyboard(user.language)
        )
    
    logger.info(f"User {user.telegram_id} started the bot")


@router.message(F.text.in_(["🌐 Змінити мову", "🌐 Sprache ändern"]))
async def change_language(message: Message, state: FSMContext):
    """Handle language change request."""
    await message.answer(
        "Please select your preferred language / Будь ласка, виберіть мову / Bitte wählen Sie Ihre bevorzugte Sprache:",
        reply_markup=get_language_keyboard()
    )
    await state.set_state(UserStates.selecting_language)
    
    logger.info(f"User {message.from_user.id} requested language change")


@router.message(UserStates.selecting_language, F.text.startswith(("🇺🇦", "🇩🇪")))
async def process_language_selection(message: Message, state: FSMContext, session_pool):
    """Process language selection."""
    language = None
    
    if message.text.startswith("🇺🇦"):
        language = "uk"
    elif message.text.startswith("🇩🇪"):
        language = "de"
    
    if language:
        # Update user's language preference
        async with session_pool() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_telegram_id(message.from_user.id)
            if user:
                user.language = language
                await user_repo.update(user)
                await user_repo.commit()
        
        # Clear the state
        await state.clear()
        
        # Send welcome message with the selected language
        await message.answer(
            format_welcome_message(message.from_user.full_name, language),
            reply_markup=get_main_keyboard(language)
        )
        
        logger.info(f"User {message.from_user.id} selected language: {language}")
    else:
        # Invalid language selection
        await message.answer(
            "Please select a valid language option.",
            reply_markup=get_language_keyboard()
        )


@router.message(Command("help"))
async def cmd_help(message: Message, session_pool):
    """Handle the /help command."""
    # Get user's language preference
    language = "uk"  # Default to Ukrainian
    
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        if user and user.language:
            language = user.language
    
    await message.answer(
        format_help_message(language),
        reply_markup=get_main_keyboard(language)
    )
    
    logger.info(f"User {message.from_user.id} requested help")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext, session_pool):
    """Handle the /cancel command."""
    # Get the current state
    current_state = await state.get_state()
    
    if current_state is None:
        # Get user's language preference
        language = "uk"  # Default to Ukrainian
        
        async with session_pool() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_telegram_id(message.from_user.id)
            if user and user.language:
                language = user.language
        
        cancel_message = "Немає активної операції для скасування."
        if language == "de":
            cancel_message = "Kein aktiver Vorgang zum Abbrechen."
        
        await message.answer(
            cancel_message,
            reply_markup=get_main_keyboard(language)
        )
        return
    
    # Cancel the state
    await state.clear()
    
    # Get user's language preference
    language = "uk"  # Default to Ukrainian
    
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        if user and user.language:
            language = user.language
    
    cancel_message = "Операцію скасовано. Ви можете почати спочатку."
    if language == "de":
        cancel_message = "Vorgang abgebrochen. Sie können neu beginnen."
    
    await message.answer(
        cancel_message,
        reply_markup=get_main_keyboard(language)
    )
    
    logger.info(f"User {message.from_user.id} canceled state {current_state}")


@router.message(F.text.in_(["❌ Скасувати", "❌ Abbrechen"]))
async def cancel_button(message: Message, state: FSMContext, session_pool):
    """Handle the cancel button."""
    await cmd_cancel(message, state, session_pool)


@router.message(F.text.in_(["🏠 Головне меню", "🏠 Hauptmenü"]))
async def main_menu_button(message: Message, state: FSMContext, session_pool):
    """Handle the main menu button."""
    # Clear any active state
    await state.clear()
    
    # Get user's language preference
    language = "uk"  # Default to Ukrainian
    
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        if user and user.language:
            language = user.language
    
    # Prepare main menu message based on language
    menu_text = "Головне меню"
    if language == "de":
        menu_text = "Hauptmenü"
    
    await message.answer(
        menu_text,
        reply_markup=get_main_keyboard(language)
    )
    
    logger.info(f"User {message.from_user.id} returned to main menu") 