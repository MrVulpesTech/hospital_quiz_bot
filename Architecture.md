# Hospital Quiz Bot Architecture

## Overview
The Hospital Quiz Bot is a Telegram bot built using aiogram and OpenAI's GPT API. It presents users with a series of medical questions regarding knee examinations, collects their answers, and uses these responses to generate a comprehensive medical report.

## Core Components

### 1. Bot Framework
- Built using **aiogram 3.x** - the modern asynchronous framework for Telegram Bot API
- Uses FSM (Finite State Machine) for managing conversation flow

### 2. Data Storage
- SQLite database for storing:
  - User information
  - Session data
  - Quiz responses
  - Generated reports

### 3. Question Management
- Structured question format in YAML/JSON
- Support for different question types (multiple choice, text input)
- Flexible keyboard layouts for response options

### 4. OpenAI Integration
- API client for communicating with OpenAI's GPT-4-mini model
- Prompt engineering for optimal medical report generation
- Error handling and retry mechanisms

### 5. User Interface
- Interactive buttons for answering questions
- Progress indicators
- Report viewing and sharing functionality

## Data Flow

1. **Initialization**
   - User starts the bot with /start
   - Bot introduces itself and explains the purpose
   - Bot offers to begin the quiz

2. **Quiz Flow**
   - Bot sequentially asks predefined questions
   - User selects answers from provided options
   - Responses are stored in a session/database
   - Bot tracks progress through the quiz

3. **Report Generation**
   - When all questions are answered, data is compiled
   - Structured prompt is sent to OpenAI API
   - Generated medical report is received

4. **Delivery & Persistence**
   - Formatted report is presented to the user
   - Report is stored for future reference
   - User can request previous reports

## Technical Implementation

### Environment
- Python 3.9+
- Asynchronous programming using asyncio
- Docker container for deployment (optional)

### Dependencies
- aiogram 3.x: Telegram Bot framework
- SQLAlchemy/aiosqlite: Database ORM/connector
- pydantic: Data validation and settings management
- OpenAI Python SDK: API integration
- python-dotenv: Environment variable management
- logging: Comprehensive logging system

### Configuration
- Environment variables for sensitive information
- Configuration files for bot behavior
- Separated development and production environments 