"""Application configuration module."""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_BEARER_TOKEN: str
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # Pinecone Configuration
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    
    # PostgreSQL Configuration
    DATABASE_URL: str
    
    # Application Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Document Storage
    DOCUMENT_STORAGE_PATH: str = "storage/documents"
    
    class Config:
        """Pydantic config."""
        
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Ensure document storage directory exists
os.makedirs(settings.DOCUMENT_STORAGE_PATH, exist_ok=True)
