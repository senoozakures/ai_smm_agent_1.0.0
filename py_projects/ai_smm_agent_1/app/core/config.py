from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "SMM AI Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smm_agent.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # DALL-E
    DALL_E_MODEL: str = "dall-e-3"
    DALL_E_SIZE: str = "1024x1024"
    DALL_E_QUALITY: str = "standard"
    
    # Социальные сети
    INSTAGRAM_USERNAME: Optional[str] = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD: Optional[str] = os.getenv("INSTAGRAM_PASSWORD")
    
    FACEBOOK_ACCESS_TOKEN: Optional[str] = os.getenv("FACEBOOK_ACCESS_TOKEN")
    FACEBOOK_PAGE_ID: Optional[str] = os.getenv("FACEBOOK_PAGE_ID")
    
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHANNEL_ID: Optional[str] = os.getenv("TELEGRAM_CHANNEL_ID")
    TELEGRAM_CTA_SUFFIX: Optional[str] = os.getenv("TELEGRAM_CTA_SUFFIX")
    
    # Настройки контента
    DEFAULT_POST_LENGTH: int = 200
    MAX_POST_LENGTH: int = 500
    DEFAULT_HASHTAGS_COUNT: int = 5
    MAX_HASHTAGS_COUNT: int = 10
    
    # Планировщик
    DEFAULT_POSTING_TIME: str = "10:00"
    POSTING_INTERVAL_HOURS: int = 24
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Логирование
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"


settings = Settings()
