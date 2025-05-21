# Hospital Quiz Bot

A Telegram bot for conducting medical knee examination quizzes and generating professional medical reports using OpenAI's GPT API.

## Description

This bot conducts structured medical quizzes specifically for knee examinations in Ukrainian. It collects user responses through an interactive Telegram interface and uses OpenAI's GPT-4o-mini model to generate human-like, professional medical reports based on the examination data.

### Key Features

- Interactive quiz interface with response buttons
- Step-by-step guided medical examination process
- Session management to save progress
- AI-powered report generation
- Previous reports storage and retrieval
- User-friendly Ukrainian language interface

## Technology Stack

- **Python 3.9+**: Core programming language
- **aiogram 3.x**: Modern asynchronous framework for Telegram Bot API
- **SQLAlchemy**: SQL toolkit and ORM for database management
- **aiosqlite**: Asynchronous SQLite database client
- **OpenAI API**: Integration with GPT-4o-mini for report generation
- **pydantic**: Data validation and settings management

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))
- OpenAI API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hospital_quiz_bot.git
cd hospital_quiz_bot
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with the following variables:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
ADMIN_USER_ID=your_telegram_user_id
```

### Running the Bot

1. Start the bot:
```bash
python bot.py
```

2. Open Telegram and search for your bot by its username
3. Start a conversation with the bot by sending the `/start` command

## Usage

### Basic Commands

- `/start` - Start the bot and get welcome message
- `/help` - Show help information
- `/quiz` - Begin a new knee examination quiz
- `/reports` - View your previous reports
- `/cancel` - Cancel the current operation

### Quiz Flow

1. Start a new quiz with `/quiz`
2. Answer each question using the provided buttons
3. For angle measurements, enter the values in the requested format
4. Complete all questions to generate the report
5. View the generated medical report
6. Optionally save or share the report

## Development

### Project Structure

See the `project_structure.md` file for a detailed overview of the project organization.

### Testing

Run the test suite with:
```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for providing the GPT API
- Telegram for the Bot API
- Contributors to the aiogram framework 