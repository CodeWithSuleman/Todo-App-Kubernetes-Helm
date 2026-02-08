"""
Configuration settings for the Todo Web Application
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days (7 * 24 * 60 = 10080 minutes)

    # Application settings
    APP_NAME: str = "Todo Web Application"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    API_V1_STR: str = "/api/v1"

    # CORS settings - allowed origins
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "https://hackathon-2-phase-iii-chi.vercel.app/"
    ).split(",")

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create a single instance of settings
settings = Settings()