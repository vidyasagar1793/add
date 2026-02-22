import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Content Aggregator"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_TO_A_SECURE_RANDOM_KEY_IN_PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    class Config:
        env_file = ".env"

settings = Settings()
