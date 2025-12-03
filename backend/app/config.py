import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    
    # Model Configuration
    WHISPER_MODEL: str = "whisper-large-v3"
    LLM_MODEL: str = "llama-3.1-8b-instant"
    
    # Supported Languages
    SUPPORTED_LANGUAGES: dict = {
        "en": {"name": "English", "voice": "en-US-AriaNeural"},
        "hi": {"name": "Hindi", "voice": "hi-IN-SwaraNeural"},
        "es": {"name": "Spanish", "voice": "es-ES-ElviraNeural"},
        "fr": {"name": "French", "voice": "fr-FR-DeniseNeural"},
        "de": {"name": "German", "voice": "de-DE-KatjaNeural"},
        "pt": {"name": "Portuguese", "voice": "pt-BR-FranciscaNeural"},
        "it": {"name": "Italian", "voice": "it-IT-ElsaNeural"},
        "ja": {"name": "Japanese", "voice": "ja-JP-NanamiNeural"},
        "ko": {"name": "Korean", "voice": "ko-KR-SunHiNeural"},
        "zh": {"name": "Chinese", "voice": "zh-CN-XiaoxiaoNeural"},
    }
    
    # Application Settings
    MAX_AUDIO_SIZE_MB: int = 25
    SESSION_TIMEOUT_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

