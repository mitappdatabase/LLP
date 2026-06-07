"""
Core Configuration for Innovate Enterprise LLP Backend
Handles environment variables, security settings, and application configuration
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Settings
    APP_NAME: str = "Innovate Enterprise LLP API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Backend API for Innovate Enterprise LLP - Electronics, IoT, AI & Agricultural Solutions"
    DEBUG: bool = False
    
    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/innovate_enterprise"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://innovateenterprise.com",
        "https://www.innovateenterprise.com"
    ]
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "jpg", "jpeg", "png", "gif", "doc", "docx"]
    UPLOAD_DIR: str = "/app/uploads"
    
    # Email Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@innovateenterprise.com"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Multi-language Support
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: List[str] = ["en", "mr"]  # English and Marathi
    
    # Weather Station API
    WEATHER_API_KEY: Optional[str] = None
    WEATHER_API_URL: str = "https://api.weatherapi.com/v1"
    
    # S3 Storage (Future)
    USE_S3: bool = False
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: Optional[str] = None
    AWS_REGION: str = "ap-south-1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
