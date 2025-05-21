# Hospital Quiz Bot Project Structure

This document outlines the recommended file structure for the Hospital Quiz Bot project.

```
hospital_quiz_bot/
│
├── .env                      # Environment variables (API keys, tokens)
├── .gitignore                # Git ignore file
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
│
├── bot.py                    # Main entry point for the bot
│
├── config/
│   ├── __init__.py
│   ├── settings.py           # Bot configuration settings
│   └── logging_config.py     # Logging configuration
│
├── data/
│   ├── quizes.yaml           # Quiz questions and options
│   └── prompts.md            # OpenAI prompt templates
│
├── app/
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py           # Base DB model
│   │   ├── user.py           # User model
│   │   └── quiz_response.py  # Quiz response model
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py     # Database connection handling
│   │   └── repository.py     # Data access patterns
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── openai_service.py # OpenAI API integration
│   │   ├── quiz_service.py   # Quiz management logic
│   │   └── report_service.py # Report generation service
│   │
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── base.py           # Base handler class
│   │   ├── commands.py       # Command handlers (/start, /help, etc.)
│   │   ├── quiz.py           # Quiz flow handlers
│   │   └── report.py         # Report viewing handlers
│   │
│   ├── keyboards/
│   │   ├── __init__.py
│   │   ├── reply.py          # Reply keyboard layouts
│   │   └── inline.py         # Inline keyboard layouts
│   │
│   ├── states/
│   │   ├── __init__.py
│   │   └── quiz_states.py    # FSM states for quiz flow
│   │
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py     # Text formatting helpers
│       ├── validators.py     # Input validation 
│       └── logger.py         # Logging utilities
│
└── tests/
    ├── __init__.py
    ├── conftest.py           # Test fixtures
    ├── test_quiz_flow.py     # Quiz flow tests
    └── test_openai.py        # OpenAI integration tests
```

## Key Components

### Main Files
- `bot.py`: Entry point for the application, initializes the bot and starts polling
- `.env`: Configuration file for environment variables (Telegram token, OpenAI API key)
- `requirements.txt`: Lists all Python dependencies

### Config
- Centralized configuration management
- Environment-specific settings
- Logging configuration

### Data
- Contains data files like the quiz questions and prompt templates
- Keeps data separate from code

### App
The core application is organized into several modules:

#### Models
- Database models using SQLAlchemy
- Represents users, quiz responses, and other entities

#### Database
- Connection management
- Repository pattern for data access
- Transaction handling

#### Services
- Business logic implementation
- External API integrations (OpenAI)
- Core functionality services

#### Handlers
- Telegram message and callback handlers
- Organized by feature/functionality
- Command handlers for bot commands

#### Keyboards
- Reply and inline keyboard layouts
- Keyboard generation functions

#### States
- Finite State Machine states for conversation flow
- State transition logic

#### Utils
- Helper functions and utilities
- Text formatting, validation, logging

### Tests
- Comprehensive test suite
- Test fixtures and utilities
- Integration and unit tests 