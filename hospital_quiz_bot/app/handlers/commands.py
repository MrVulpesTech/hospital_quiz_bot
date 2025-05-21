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
from hospital_quiz_bot.app.keyboards.reply import get_main_keyboard, remove_keyboard
from hospital_quiz_bot.config.logging_config import logger

# Create a router for command handlers
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session_pool):
    """Handle the /start command."""
    # Create a session and get/create the user
    async with session_pool() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_or_create_user(message.from_user)
    
    # Send welcome message
    await message.answer(
        format_welcome_message(user.full_name),
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"User {user.telegram_id} started the bot")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle the /help command."""
    await message.answer(
        format_help_message(),
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"User {message.from_user.id} requested help")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Handle the /cancel command."""
    # Get the current state
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer(
            "Немає активної операції для скасування.",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Cancel the state
    await state.clear()
    
    await message.answer(
        "Операцію скасовано. Ви можете почати спочатку.",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"User {message.from_user.id} canceled state {current_state}")


@router.message(F.text == "❌ Скасувати")
async def cancel_button(message: Message, state: FSMContext):
    """Handle the cancel button."""
    await cmd_cancel(message, state)


@router.message(F.text == "🏠 Головне меню")
async def main_menu_button(message: Message, state: FSMContext):
    """Handle the main menu button."""
    # Clear any active state
    await state.clear()
    
    await message.answer(
        "Головне меню",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"User {message.from_user.id} returned to main menu") 