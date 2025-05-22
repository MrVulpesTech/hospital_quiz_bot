"""
Quiz states for the Hospital Quiz Bot.
This module defines the FSM states for the quiz conversation flow.
"""

from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    """FSM states for user-specific operations."""
    
    # Language selection
    selecting_language = State()


class QuizStates(StatesGroup):
    """FSM states for the quiz conversation flow."""
    
    # Initial state
    start = State()
    
    # Answering questions
    answering = State()
    
    # Optional text input for follow-up questions
    text_input = State()
    
    # Confirmation before generating the report
    confirmation = State()
    
    # Report generation
    generating_report = State()
    
    # Viewing the report
    viewing_report = State()
    
    # Share options
    sharing = State()


class ReportStates(StatesGroup):
    """FSM states for viewing previous reports."""
    
    # Listing reports
    listing = State()
    
    # Viewing a specific report
    viewing = State()
    
    # Sharing a report
    sharing = State() 