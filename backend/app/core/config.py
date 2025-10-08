"""
Configuration settings for PesoScan API
"""

import os
from typing import List

class Settings:
    # API Settings
    APP_NAME: str = "PesoScan API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ]
    
    # Model Paths
    YOLO_MODEL_PATH: str = "trained_models/peso_detection.pt"
    CNN_MODEL_PATH: str = "trained_models/peso_classifier.pt"
    
    # Image Processing Settings
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_FORMATS: List[str] = ["jpg", "jpeg", "png", "bmp"]
    PROCESSED_IMAGE_SIZE: tuple = (640, 640)
    
    # Detection Settings
    DETECTION_CONFIDENCE_THRESHOLD: float = 0.5
    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Database Settings (for future use)
    DATABASE_URL: str = "sqlite:///./pesoscan.db"
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/pesoscan.log"

# Create settings instance
settings = Settings()

# Ensure required directories exist
os.makedirs("trained_models", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("temp", exist_ok=True)