from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    
    API_TITLE: str = "Supplier Risk Prediction API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for predicting supplier risk levels"
    
    MODEL_PATH: str = "models/best_model.pkl"
    LABEL_ENCODER_PATH: str = "models/label_encoder.pkl"
    SCALER_PATH: str = "models/scaler.pkl"
    LABEL_ENCODERS_PATH: str = "models/label_encoders.pkl"
    
    DATA_RAW_PATH: str = "data/raw"
    DATA_PROCESSED_PATH: str = "data/processed"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:8501",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignorer les variables non définies

settings = Settings()