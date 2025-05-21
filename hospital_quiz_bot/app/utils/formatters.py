"""
Formatters for the Hospital Quiz Bot.
This module provides utility functions for formatting text in messages.
"""

from typing import Dict, Any, List, Optional
import re

from aiogram.utils.markdown import hbold, hitalic, hunderline, hcode, hlink, hpre


def format_welcome_message(user_name: str) -> str:
    """Format the welcome message."""
    return (
        f"Вітаю, {hbold(user_name)}! 👋\n\n"
        f"Я - бот для проведення медичного опитування і генерації звітів обстеження колінного суглоба.\n\n"
        f"Щоб почати нове опитування, введіть команду {hcode('/quiz')}\n"
        f"Для перегляду попередніх звітів, введіть {hcode('/reports')}\n"
        f"Для отримання довідки, введіть {hcode('/help')}"
    )


def format_help_message() -> str:
    """Format the help message."""
    return (
        f"{hbold('Довідка по використанню бота')}\n\n"
        f"{hbold('Основні команди:')}\n"
        f"• {hcode('/start')} - Запустити бота і отримати привітання\n"
        f"• {hcode('/quiz')} - Почати нове опитування\n"
        f"• {hcode('/reports')} - Переглянути попередні звіти\n"
        f"• {hcode('/help')} - Показати цю довідку\n"
        f"• {hcode('/cancel')} - Скасувати поточну операцію\n\n"
        f"{hbold('Підказки:')}\n"
        f"• Ви можете скасувати опитування в будь-який момент, натиснувши '❌ Скасувати'\n"
        f"• На питання з форматом введення, вводьте дані точно в запропонованому форматі\n"
        f"• Звіти зберігаються і доступні для перегляду в будь-який час через команду {hcode('/reports')}"
    )


def format_quiz_start_message() -> str:
    """Format the quiz start message."""
    return (
        f"{hbold('Опитування про стан колінного суглоба')}\n\n"
        f"Я задам вам серію запитань про стан колінного суглоба пацієнта.\n"
        f"На основі ваших відповідей буде згенеровано професійний медичний звіт.\n\n"
        f"Відповідайте на запитання, використовуючи кнопки або вводячи текст, де це потрібно.\n"
        f"Ви можете скасувати опитування в будь-який момент, натиснувши '❌ Скасувати'.\n\n"
        f"{hbold('Почнімо!')}"
    )


def format_question(
    question_text: str,
    current_index: int,
    total_questions: int,
) -> str:
    """Format a question message."""
    progress = f"Питання {current_index + 1}/{total_questions}"
    return f"{hbold(progress)}\n\n{question_text}"


def format_quiz_confirmation_message(responses: Dict[str, str], questions: List[Dict[str, Any]]) -> str:
    """Format the quiz confirmation message."""
    # Create a mapping of question ID to text
    question_map = {q["id"]: q["text"] for q in questions}
    
    # Format the responses
    formatted_responses = []
    for question_id, answer in responses.items():
        question_text = question_map.get(question_id, question_id)
        formatted_responses.append(f"• {question_text}: {hbold(answer)}")
    
    return (
        f"{hbold('Перевірте ваші відповіді')}\n\n"
        f"{hitalic('Переконайтеся, що всі відповіді правильні, перш ніж продовжити.')}\n\n"
        f"{chr(10).join(formatted_responses)}\n\n"
        f"Бажаєте завершити опитування і згенерувати звіт?"
    )


def format_report_generation_message() -> str:
    """Format the report generation message."""
    return (
        f"{hbold('Генерую звіт...')}\n\n"
        f"Будь ласка, зачекайте. Це може зайняти кілька секунд."
    )


def format_report_message(report: str) -> str:
    """Format the report message."""
    # Check if report is too long for a single message
    if len(report) > 4000:
        # Split into parts (preserving paragraph breaks)
        parts = split_long_text(report, 4000)
        formatted_parts = []
        
        for i, part in enumerate(parts):
            if i == 0:
                header = f"{hbold('📋 Медичний звіт')} (Частина {i+1}/{len(parts)})\n\n"
            else:
                header = f"{hbold('📋 Медичний звіт')} (Продовження, частина {i+1}/{len(parts)})\n\n"
            
            formatted_parts.append(f"{header}{part}")
        
        return formatted_parts
    
    return f"{hbold('📋 Медичний звіт')}\n\n{report}"


def format_reports_list_message(count: int) -> str:
    """Format the reports list message."""
    if count == 0:
        return (
            f"{hbold('Ваші звіти')}\n\n"
            f"У вас ще немає збережених звітів. Щоб створити звіт, почніть нове опитування командою {hcode('/quiz')}."
        )
    
    return (
        f"{hbold('Ваші звіти')}\n\n"
        f"У вас є {count} збережених звітів. Виберіть звіт для перегляду:"
    )


def split_long_text(text: str, max_length: int) -> List[str]:
    """Split long text into parts while preserving paragraph breaks."""
    # If text is shorter than max_length, return it as is
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_part = ""
    
    # Split by paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed max_length, start a new part
        if len(current_part) + len(paragraph) + 2 > max_length and current_part:
            parts.append(current_part.strip())
            current_part = paragraph + "\n\n"
        else:
            current_part += paragraph + "\n\n"
    
    # Add the last part if it's not empty
    if current_part:
        parts.append(current_part.strip())
    
    return parts 