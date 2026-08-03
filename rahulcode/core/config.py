"""
SmartCampus AI - Application Configuration
Reads environment variables and initializes core application settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    APP_NAME: str = os.getenv("APP_NAME", "SmartCampus AI")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_smartcampus_secret_2026")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    DATABASE_DIR: Path = BASE_DIR / "database"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    
    # AI Default Model
    OPENAI_MODEL: str = "gpt-4o-mini"
