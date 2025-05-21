"""
Reply keyboard layouts for the Hospital Quiz Bot.
This module provides functions for creating reply keyboard markups.
"""

from typing import List, Optional

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get the main keyboard with primary commands."""
    keyboard = [
        [KeyboardButton(text="/quiz")],
        [KeyboardButton(text="/reports"), KeyboardButton(text="/help")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_quiz_options_keyboard(options: List[str], row_width: int = 2) -> ReplyKeyboardMarkup:
    """Get a keyboard with quiz options."""
    # Split options into rows based on row_width
    rows = []
    for i in range(0, len(options), row_width):
        row = []
        for option in options[i:i+row_width]:
            row.append(KeyboardButton(text=option))
        rows.append(row)
        
    # Add navigation buttons at the bottom
    rows.append([
        KeyboardButton(text="⬅️ Назад"),
        KeyboardButton(text="❌ Скасувати"),
    ])
    
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_confirmation_keyboard() -> ReplyKeyboardMarkup:
    """Get a keyboard for confirmation."""
    keyboard = [
        [KeyboardButton(text="✅ Так, завершити")],
        [KeyboardButton(text="⬅️ Повернутися до питань")],
        [KeyboardButton(text="❌ Скасувати")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Get a keyboard with just a cancel button."""
    keyboard = [
        [KeyboardButton(text="❌ Скасувати")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_report_actions_keyboard() -> ReplyKeyboardMarkup:
    """Get a keyboard for report actions."""
    keyboard = [
        # Comment out "Поділитися" button for now
        # [KeyboardButton(text="📋 Зберегти звіт"), KeyboardButton(text="📤 Поділитися")],
        [KeyboardButton(text="📋 Зберегти звіт")],
        [KeyboardButton(text="/quiz")],  # Replace with direct command for new quiz
        [KeyboardButton(text="🏠 Головне меню")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    """Remove the keyboard."""
    return ReplyKeyboardRemove() 