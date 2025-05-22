"""
Settings configuration for the Hospital Quiz Bot.
This module loads environment variables and provides configuration settings for the bot.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Determine the base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")


class TelegramSettings(BaseModel):
    """Telegram bot settings"""
    token: str = Field(..., description="Telegram Bot API token")
    admin_user_id: Optional[int] = Field(None, description="Admin user ID for special commands")
    polling_timeout: int = Field(30, description="Polling timeout in seconds")


class DatabaseSettings(BaseModel):
    """Database connection settings"""
    url: str = Field("sqlite:///bot_database.db", description="Database connection URL")
    echo: bool = Field(False, description="Echo SQL statements")


class OpenAISettings(BaseModel):
    """OpenAI API settings"""
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field("gpt-4o-mini", description="OpenAI model to use")
    temperature: float = Field(0.7, description="Temperature for response generation")
    max_tokens: int = Field(2000, description="Maximum tokens in response")
    top_p: float = Field(0.95, description="Top-p sampling parameter")


class AppSettings(BaseModel):
    """Application settings"""
    telegram: TelegramSettings
    database: DatabaseSettings
    openai: OpenAISettings
    quiz_file: Path = Field(BASE_DIR / "data" / "quizes.yaml", description="Path to quiz questions file")
    prompts_file: Path = Field(BASE_DIR / "data" / "prompts.md", description="Path to prompts file")
    log_level: str = Field("INFO", description="Logging level")


def load_settings() -> AppSettings:
    """Load settings from environment variables"""
    return AppSettings(
        telegram=TelegramSettings(
            token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            admin_user_id=int(os.getenv("ADMIN_USER_ID", "0")) if os.getenv("ADMIN_USER_ID") else None,
            polling_timeout=int(os.getenv("POLLING_TIMEOUT", "30")),
        ),
        database=DatabaseSettings(
            url=os.getenv("DATABASE_URL", "sqlite:///" + str(BASE_DIR / "bot_database.db")),
            echo=os.getenv("DATABASE_ECHO", "False").lower() == "true",
        ),
        openai=OpenAISettings(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
            top_p=float(os.getenv("OPENAI_TOP_P", "0.95")),
        ),
        quiz_file=Path(os.getenv("QUIZ_FILE", str(BASE_DIR / "data" / "quizes.yaml"))),
        prompts_file=Path(os.getenv("PROMPTS_FILE", str(BASE_DIR / "data" / "prompts.md"))),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


# Create a singleton instance of the settings
settings = load_settings() 