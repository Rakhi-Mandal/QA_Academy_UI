"""
Application Configuration
Loads environment variables and provides configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings from environment variables"""
    
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "qe_academy")
    
    # App Configuration
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # File Upload Configuration
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "5242880"))  # 5MB default
    ALLOWED_EXTENSIONS: set = set(os.getenv("ALLOWED_EXTENSIONS", "pdf,jpg,jpeg,png").split(","))
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.APP_ENV == "development"

# Create settings instance
settings = Settings()