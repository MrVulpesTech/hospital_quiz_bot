"""
Settings configuration for the Hospital Quiz Bot.
This module loads environment variables and provides configuration settings for the bot.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Determine the base directory of the project
BASE_DIR = Path(__file__).parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Try to load environment variables from .env file first
load_dotenv(PROJECT_ROOT / ".env", override=True)

# Then try to load from config.yaml if it exists
CONFIG_YAML_PATH = PROJECT_ROOT / "config.yaml"
yaml_config = {}
if CONFIG_YAML_PATH.exists():
    with open(CONFIG_YAML_PATH, "r", encoding="utf-8") as f:
        yaml_config = yaml.safe_load(f) or {}


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
    quiz_file: Path = Field(PROJECT_ROOT / "quizes.yaml", description="Path to quiz questions file")
    quiz_file_de: Optional[Path] = Field(PROJECT_ROOT / "quizes_de.yaml", description="Path to German quiz questions file")
    prompts_file: Path = Field(PROJECT_ROOT / "prompts.md", description="Path to prompts file")
    log_level: str = Field("INFO", description="Logging level")


def load_settings() -> AppSettings:
    """Load settings from environment variables and/or YAML config"""
    
    # Get telegram settings
    telegram_config = yaml_config.get("telegram", {})
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN") or telegram_config.get("token", "")
    admin_user_id_str = os.getenv("ADMIN_USER_ID") or str(telegram_config.get("admin_user_id", "0"))
    admin_user_id = int(admin_user_id_str) if admin_user_id_str and admin_user_id_str != "None" else None
    polling_timeout = int(os.getenv("POLLING_TIMEOUT", str(telegram_config.get("polling_timeout", "30"))))
    
    # Get database settings
    db_config = yaml_config.get("database", {})
    db_url = os.getenv("DATABASE_URL") or db_config.get("url", "sqlite:///" + str(PROJECT_ROOT / "bot_database.db"))
    db_echo = os.getenv("DATABASE_ECHO", str(db_config.get("echo", "False"))).lower() == "true"
    
    # Get OpenAI settings
    openai_config = yaml_config.get("openai", {})
    openai_api_key = os.getenv("OPENAI_API_KEY") or openai_config.get("api_key", "")
    openai_model = os.getenv("OPENAI_MODEL") or openai_config.get("model", "gpt-4o-mini")
    openai_temp = float(os.getenv("OPENAI_TEMPERATURE") or str(openai_config.get("temperature", "0.7")))
    openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS") or str(openai_config.get("max_tokens", "2000")))
    openai_top_p = float(os.getenv("OPENAI_TOP_P") or str(openai_config.get("top_p", "0.95")))
    
    # Get app settings
    app_config = yaml_config.get("app", {})
    quiz_file = os.getenv("QUIZ_FILE") or app_config.get("quiz_file", str(PROJECT_ROOT / "quizes.yaml"))
    quiz_file_de = os.getenv("QUIZ_FILE_DE") or app_config.get("quiz_file_de", str(PROJECT_ROOT / "quizes_de.yaml"))
    prompts_file = os.getenv("PROMPTS_FILE") or app_config.get("prompts_file", str(PROJECT_ROOT / "prompts.md"))
    log_level = os.getenv("LOG_LEVEL") or app_config.get("log_level", "INFO")
    
    return AppSettings(
        telegram=TelegramSettings(
            token=telegram_token,
            admin_user_id=admin_user_id,
            polling_timeout=polling_timeout,
        ),
        database=DatabaseSettings(
            url=db_url,
            echo=db_echo,
        ),
        openai=OpenAISettings(
            api_key=openai_api_key,
            model=openai_model,
            temperature=openai_temp,
            max_tokens=openai_max_tokens,
            top_p=openai_top_p,
        ),
        quiz_file=Path(quiz_file),
        quiz_file_de=Path(quiz_file_de) if quiz_file_de else None,
        prompts_file=Path(prompts_file),
        log_level=log_level,
    )


# Create a singleton instance of the settings
settings = load_settings() 