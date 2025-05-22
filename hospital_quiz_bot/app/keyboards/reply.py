"""
Reply keyboard layouts for the Hospital Quiz Bot.
This module provides functions for creating reply keyboard markups.
"""

from typing import List, Optional

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_language_keyboard() -> ReplyKeyboardMarkup:
    """Get a keyboard for language selection."""
    keyboard = [
        [KeyboardButton(text="🇺🇦 Українська")],
        [KeyboardButton(text="🇩🇪 Deutsch")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_main_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """Get the main keyboard with primary commands."""
    if language == "de":
        keyboard = [
            [KeyboardButton(text="/quiz")],
            [KeyboardButton(text="/reports"), KeyboardButton(text="/help")],
            [KeyboardButton(text="🌐 Sprache ändern")],
        ]
    else:  # Default to Ukrainian
        keyboard = [
            [KeyboardButton(text="/quiz")],
            [KeyboardButton(text="/reports"), KeyboardButton(text="/help")],
            [KeyboardButton(text="🌐 Змінити мову")],
        ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_quiz_options_keyboard(options: List[str], language: str = "uk", row_width: int = 2) -> ReplyKeyboardMarkup:
    """Get a keyboard with quiz options."""
    # Split options into rows based on row_width
    rows = []
    for i in range(0, len(options), row_width):
        row = []
        for option in options[i:i+row_width]:
            row.append(KeyboardButton(text=option))
        rows.append(row)
    
    # Set navigation button text based on language
    back_text = "⬅️ Назад"
    cancel_text = "❌ Скасувати"
    
    if language == "de":
        back_text = "⬅️ Zurück"
        cancel_text = "❌ Abbrechen"
    
    # Add navigation buttons at the bottom
    rows.append([
        KeyboardButton(text=back_text),
        KeyboardButton(text=cancel_text),
    ])
    
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_confirmation_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """Get a keyboard for confirmation."""
    if language == "de":
        keyboard = [
            [KeyboardButton(text="✅ Ja, abschließen")],
            [KeyboardButton(text="⬅️ Zurück zu den Fragen")],
            [KeyboardButton(text="❌ Abbrechen")],
        ]
    else:  # Default to Ukrainian
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


def get_cancel_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """Get a keyboard with just a cancel button."""
    cancel_text = "❌ Скасувати"
    if language == "de":
        cancel_text = "❌ Abbrechen"
    
    keyboard = [
        [KeyboardButton(text=cancel_text)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_report_actions_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """Get a keyboard for report actions."""
    if language == "de":
        keyboard = [
            [KeyboardButton(text="📋 Bericht speichern")],
            [KeyboardButton(text="/quiz")],  # Replace with direct command for new quiz
            [KeyboardButton(text="🏠 Hauptmenü")],
        ]
    else:  # Default to Ukrainian
        keyboard = [
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