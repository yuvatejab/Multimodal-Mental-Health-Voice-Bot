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
    
    # Supported Languages with emotional voice profiles
    SUPPORTED_LANGUAGES: dict = {
        "en": {
            "name": "English",
            "voice": "en-US-AriaNeural",
            "emotional_voices": {
                "empathetic": "en-US-AriaNeural",
                "cheerful": "en-US-JennyNeural",
                "calm": "en-US-GuyNeural",
                "gentle": "en-US-AriaNeural",
                "supportive": "en-US-JennyNeural",
                "friendly": "en-US-AriaNeural"
            }
        },
        "hi": {
            "name": "Hindi",
            "voice": "hi-IN-SwaraNeural",
            "emotional_voices": {
                "empathetic": "hi-IN-SwaraNeural",
                "calm": "hi-IN-MadhurNeural",
                "gentle": "hi-IN-SwaraNeural",
                "supportive": "hi-IN-SwaraNeural",
                "friendly": "hi-IN-SwaraNeural"
            }
        },
        "es": {
            "name": "Spanish",
            "voice": "es-ES-ElviraNeural",
            "emotional_voices": {
                "empathetic": "es-ES-ElviraNeural",
                "cheerful": "es-MX-DaliaNeural",
                "calm": "es-ES-AlvaroNeural",
                "gentle": "es-ES-ElviraNeural",
                "supportive": "es-ES-ElviraNeural",
                "friendly": "es-ES-ElviraNeural"
            }
        },
        "fr": {
            "name": "French",
            "voice": "fr-FR-DeniseNeural",
            "emotional_voices": {
                "empathetic": "fr-FR-DeniseNeural",
                "calm": "fr-FR-HenriNeural",
                "gentle": "fr-FR-DeniseNeural",
                "supportive": "fr-FR-DeniseNeural",
                "friendly": "fr-FR-DeniseNeural"
            }
        },
        "de": {
            "name": "German",
            "voice": "de-DE-KatjaNeural",
            "emotional_voices": {
                "empathetic": "de-DE-KatjaNeural",
                "calm": "de-DE-ConradNeural",
                "gentle": "de-DE-KatjaNeural",
                "supportive": "de-DE-KatjaNeural",
                "friendly": "de-DE-KatjaNeural"
            }
        },
        "pt": {
            "name": "Portuguese",
            "voice": "pt-BR-FranciscaNeural",
            "emotional_voices": {
                "empathetic": "pt-BR-FranciscaNeural",
                "calm": "pt-BR-AntonioNeural",
                "gentle": "pt-BR-FranciscaNeural",
                "supportive": "pt-BR-FranciscaNeural",
                "friendly": "pt-BR-FranciscaNeural"
            }
        },
        "it": {
            "name": "Italian",
            "voice": "it-IT-ElsaNeural",
            "emotional_voices": {
                "empathetic": "it-IT-ElsaNeural",
                "calm": "it-IT-DiegoNeural",
                "gentle": "it-IT-ElsaNeural",
                "supportive": "it-IT-ElsaNeural",
                "friendly": "it-IT-ElsaNeural"
            }
        },
        "ja": {
            "name": "Japanese",
            "voice": "ja-JP-NanamiNeural",
            "emotional_voices": {
                "empathetic": "ja-JP-NanamiNeural",
                "calm": "ja-JP-KeitaNeural",
                "gentle": "ja-JP-NanamiNeural",
                "supportive": "ja-JP-NanamiNeural",
                "friendly": "ja-JP-NanamiNeural"
            }
        },
        "ko": {
            "name": "Korean",
            "voice": "ko-KR-SunHiNeural",
            "emotional_voices": {
                "empathetic": "ko-KR-SunHiNeural",
                "calm": "ko-KR-InJoonNeural",
                "gentle": "ko-KR-SunHiNeural",
                "supportive": "ko-KR-SunHiNeural",
                "friendly": "ko-KR-SunHiNeural"
            }
        },
        "zh": {
            "name": "Chinese",
            "voice": "zh-CN-XiaoxiaoNeural",
            "emotional_voices": {
                "empathetic": "zh-CN-XiaoxiaoNeural",
                "cheerful": "zh-CN-XiaoxiaoNeural",
                "calm": "zh-CN-YunxiNeural",
                "gentle": "zh-CN-XiaoxiaoNeural",
                "supportive": "zh-CN-XiaoxiaoNeural",
                "friendly": "zh-CN-XiaoxiaoNeural"
            }
        },
    }
    
    # Application Settings
    MAX_AUDIO_SIZE_MB: int = 25
    SESSION_TIMEOUT_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

