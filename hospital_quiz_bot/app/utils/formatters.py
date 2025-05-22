"""
Formatting utility functions for the Hospital Quiz Bot.
This module provides functions for formatting messages.
"""

from typing import Dict, List, Optional, Any, Union
import re
import datetime

from aiogram.utils.markdown import hbold, hitalic, hunderline, hcode, hlink, hpre


def format_welcome_message(name: str, language: str = "uk") -> str:
    """Format the welcome message."""
    if language == "de":
        return (
            f"👋 Hallo, {name}!\n\n"
            f"Willkommen beim Hospital Quiz Bot für die Knieuntersuchung.\n\n"
            f"Sie können /quiz eingeben, um ein neues Quiz zu starten, oder /help, um Hilfe zu erhalten."
        )
    else:  # Default to Ukrainian
        return (
            f"👋 Вітаю, {name}!\n\n"
            f"Ласкаво просимо до Hospital Quiz Bot для обстеження коліна.\n\n"
            f"Ви можете ввести /quiz, щоб почати нове опитування, або /help, щоб отримати допомогу."
        )


def format_help_message(language: str = "uk") -> str:
    """Format the help message."""
    if language == "de":
        return (
            "🔍 **Hilfe zur Verwendung des Hospital Quiz Bot**\n\n"
            "Der Bot unterstützt die folgenden Befehle:\n\n"
            "• /start - Bot starten\n"
            "• /quiz - Neues Quiz starten\n"
            "• /reports - Ihre gespeicherten Berichte anzeigen\n"
            "• /help - Diese Hilfenachricht anzeigen\n"
            "• /cancel - Laufenden Vorgang abbrechen\n\n"
            "Verwenden Sie die Schaltflächen auf der Tastatur, um durch das Quiz zu navigieren."
        )
    else:  # Default to Ukrainian
        return (
            "🔍 **Допомога з використання Hospital Quiz Bot**\n\n"
            "Бот підтримує наступні команди:\n\n"
            "• /start - Запустити бота\n"
            "• /quiz - Почати нове опитування\n"
            "• /reports - Переглянути збережені звіти\n"
            "• /help - Показати це повідомлення\n"
            "• /cancel - Скасувати поточну операцію\n\n"
            "Використовуйте кнопки на клавіатурі для навігації по опитуванню."
        )


def format_quiz_start_message(language: str = "uk") -> str:
    """Format the quiz start message."""
    if language == "de":
        return (
            f"{hbold('Umfrage zum Zustand des Kniegelenks')}\n\n"
            f"Ich werde Ihnen eine Reihe von Fragen zum Zustand des Kniegelenks des Patienten stellen.\n"
            f"Basierend auf Ihren Antworten wird ein professioneller medizinischer Bericht erstellt.\n\n"
            f"Beantworten Sie die Fragen mit den Schaltflächen oder geben Sie Text ein, wo erforderlich.\n"
            f"Sie können die Umfrage jederzeit abbrechen, indem Sie auf '❌ Abbrechen' klicken.\n\n"
            f"{hbold('Beginnen wir!')}"
        )
    else:  # Default to Ukrainian
        return (
            f"{hbold('Опитування про стан колінного суглоба')}\n\n"
            f"Я задам вам серію запитань про стан колінного суглоба пацієнта.\n"
            f"На основі ваших відповідей буде згенеровано професійний медичний звіт.\n\n"
            f"Відповідайте на запитання, використовуючи кнопки або вводячи текст, де це потрібно.\n"
            f"Ви можете скасувати опитування в будь-який момент, натиснувши '❌ Скасувати'.\n\n"
            f"{hbold('Почнімо!')}"
        )


def format_question(text: str, index: int, total: int, language: str = "uk") -> str:
    """Format a question with its index."""
    if language == "de":
        return f"Frage {index + 1}/{total}:\n\n{text}"
    else:  # Default to Ukrainian
        return f"Питання {index + 1}/{total}:\n\n{text}"


def format_quiz_confirmation_message(
    responses: Dict[str, str],
    questions: List[Dict[str, Any]],
    language: str = "uk",
) -> str:
    """Format the quiz confirmation message."""
    # Create a mapping of question IDs to questions
    questions_by_id = {q["id"]: q for q in questions}
    
    # Create the header based on language
    if language == "de":
        header = "📋 **Zusammenfassung der Antworten**\n\nBitte überprüfen Sie Ihre Antworten:\n\n"
    else:  # Default to Ukrainian
        header = "📋 **Підсумок відповідей**\n\nБудь ласка, перевірте свої відповіді:\n\n"
    
    # Add each question and its response
    response_lines = []
    for question_id, response in responses.items():
        if question_id in questions_by_id:
            question_text = questions_by_id[question_id]["text"]
            response_lines.append(f"• {question_text}\n→ {response}")
    
    # Create the footer based on language
    if language == "de":
        footer = "\n\nSind Sie bereit, das Quiz abzuschließen?"
    else:  # Default to Ukrainian
        footer = "\n\nВи готові завершити опитування?"
    
    return header + "\n".join(response_lines) + footer


def format_report_generation_message(language: str = "uk") -> str:
    """Format the report generation message."""
    if language == "de":
        return "⏳ Bericht wird generiert... Bitte warten."
    else:  # Default to Ukrainian
        return "⏳ Генерація звіту... Будь ласка, зачекайте."


def format_report_message(report: Union[Dict[str, Any], str], language: str = "uk") -> Union[str, List[str]]:
    """Format the report message."""
    # If report is already a string, wrap it in a simple dictionary structure
    if isinstance(report, str):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = {
            "timestamp": current_time,
            "conclusion": report,
            "responses": {}
        }
        
    # Format based on language
    if language == "de":
        header = f"📊 **KNIEUNTERSUCHUNGSBERICHT**\n\n"
        timestamp = f"**Zeitstempel:** {report.get('timestamp', 'Nicht verfügbar')}\n"
        conclusion = f"\n**Schlussfolgerung:**\n{report.get('conclusion', 'Keine Schlussfolgerung verfügbar')}"
    else:  # Default to Ukrainian
        header = f"📊 **ЗВІТ ОБСТЕЖЕННЯ КОЛІНА**\n\n"
        timestamp = f"**Часова мітка:** {report.get('timestamp', 'Недоступно')}\n"
        conclusion = f"\n**Висновок:**\n{report.get('conclusion', 'Висновок недоступний')}"
    
    # Format the responses
    responses = report.get("responses", {})
    response_lines = []
    
    for question, answer in responses.items():
        response_lines.append(f"• **{question}**\n→ {answer}")
    
    formatted_responses = "\n".join(response_lines)
    
    # Combine all parts
    full_report = header + timestamp + formatted_responses + conclusion
    
    # Check if the report is too long
    if len(full_report) > 4096:
        # Split into multiple messages
        messages = []
        current_message = header + timestamp
        
        for line in response_lines:
            if len(current_message + line + "\n") > 4000:  # Leave some buffer
                messages.append(current_message)
                current_message = header + "**Продовження...**\n\n"
            
            current_message += line + "\n"
        
        # Add the conclusion to the last message
        current_message += conclusion
        messages.append(current_message)
        
        return messages
    else:
        return full_report


def format_reports_list_message(count: int, language: str = "uk") -> str:
    """Format the reports list message."""
    if language == "de":
        if count == 0:
            return (
                f"{hbold('Ihre Berichte')}\n\n"
                f"Sie haben noch keine gespeicherten Berichte. Um einen Bericht zu erstellen, starten Sie eine neue Umfrage mit dem Befehl {hcode('/quiz')}."
            )
        
        return (
            f"{hbold('Ihre Berichte')}\n\n"
            f"Sie haben {count} gespeicherte Berichte. Wählen Sie einen Bericht zur Ansicht:"
        )
    else:  # Default to Ukrainian
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