"""
Inline keyboard layouts for the Hospital Quiz Bot.
This module provides functions for creating inline keyboard markups.
"""

from typing import List, Dict, Any, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    prefix: str = "page"
) -> InlineKeyboardMarkup:
    """Get a pagination keyboard for navigating through pages."""
    buttons = []
    
    # Previous page button
    if current_page > 1:
        buttons.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=f"{prefix}:{current_page - 1}"
        ))
    
    # Page indicator
    buttons.append(InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data="noop"
    ))
    
    # Next page button
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(
            text="➡️",
            callback_data=f"{prefix}:{current_page + 1}"
        ))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def get_reports_keyboard(
    reports: List[Dict[str, Any]],
    page: int = 1,
    items_per_page: int = 5
) -> InlineKeyboardMarkup:
    """Get a keyboard for selecting reports."""
    # Calculate the slice for the current page
    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_reports = reports[start:end]
    
    # Create the report buttons
    buttons = []
    for report in page_reports:
        created_at = report["created_at"].strftime("%d.%m.%Y %H:%M")
        buttons.append([InlineKeyboardButton(
            text=f"Звіт від {created_at}",
            callback_data=f"report:{report['session_id']}"
        )])
    
    # Add pagination buttons if needed
    total_pages = (len(reports) + items_per_page - 1) // items_per_page
    if total_pages > 1:
        pagination = []
        
        # Previous page button
        if page > 1:
            pagination.append(InlineKeyboardButton(
                text="⬅️",
                callback_data=f"reports_page:{page - 1}"
            ))
        
        # Page indicator
        pagination.append(InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data="noop"
        ))
        
        # Next page button
        if page < total_pages:
            pagination.append(InlineKeyboardButton(
                text="➡️",
                callback_data=f"reports_page:{page + 1}"
            ))
        
        buttons.append(pagination)
    
    # Add a back button
    buttons.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_report_actions_keyboard(
    session_id: str
) -> InlineKeyboardMarkup:
    """Get a keyboard for report actions."""
    buttons = [
        [
            # Comment out the share button
            # InlineKeyboardButton(
            #     text="📤 Поділитися",
            #     callback_data=f"share:{session_id}"
            # ),
            InlineKeyboardButton(
                text="🔄 Новий звіт",
                callback_data="new_quiz"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад до списку",
                callback_data="reports"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons) 