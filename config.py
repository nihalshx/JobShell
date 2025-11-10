"""
Configuration Management for JobShell

This module provides centralized configuration management
for the JobShell application.
"""

import os
from typing import Dict, Any


class Config:
    """Application configuration class."""
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'jobshell_secret_key_2024')
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))
    SESSION_CLEANUP_INTERVAL_SECONDS = int(os.getenv('SESSION_CLEANUP_INTERVAL', 300))
    
    # Command Configuration
    MAX_COMMAND_LENGTH = int(os.getenv('MAX_COMMAND_LENGTH', 1000))
    MAX_HISTORY_SIZE = int(os.getenv('MAX_HISTORY_SIZE', 100))
    
    # Pagination Configuration
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))
    
    # Job Fetch Configuration
    DEFAULT_JOB_TYPE = os.getenv('DEFAULT_JOB_TYPE', 'internships')
    MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # CORS Configuration
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '*')
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        Get all configuration values as a dictionary.
        
        Returns:
            Dictionary containing all configuration values
        """
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration values.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            assert cls.PORT > 0 and cls.PORT < 65536, "Invalid PORT"
            assert cls.SESSION_TIMEOUT_MINUTES > 0, "Invalid SESSION_TIMEOUT"
            assert cls.MAX_COMMAND_LENGTH > 0, "Invalid MAX_COMMAND_LENGTH"
            assert cls.ITEMS_PER_PAGE > 0, "Invalid ITEMS_PER_PAGE"
            return True
        except AssertionError as e:
            print(f"Configuration validation error: {e}")
            return False


# Create a singleton instance
config = Config()


if __name__ == '__main__':
    # Test configuration
    print("JobShell Configuration:")
    print("-" * 50)
    for key, value in Config.get_all().items():
        print(f"{key}: {value}")
    print("-" * 50)
    print(f"Configuration valid: {Config.validate()}")
