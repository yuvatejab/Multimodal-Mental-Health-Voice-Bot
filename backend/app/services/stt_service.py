import os
import tempfile
from typing import Optional
from groq import Groq
from ..config import settings


class STTService:
    """Speech-to-Text service using Groq's Whisper API."""
    
    def __init__(self):
        """Initialize the STT service with Groq client."""
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.WHISPER_MODEL
    
    async def transcribe_audio(
        self, 
        audio_file: bytes, 
        language: Optional[str] = None,
        filename: str = "audio.webm"
    ) -> dict:
        """
        Transcribe audio file to text using Groq Whisper.
        
        Args:
            audio_file: Audio file bytes
            language: Optional language code (e.g., 'en', 'hi')
            filename: Original filename for format detection
            
        Returns:
            dict with 'text' and 'language' keys
        """
        try:
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                temp_file.write(audio_file)
                temp_file_path = temp_file.name
            
            try:
                # Open the file and send to Groq
                with open(temp_file_path, "rb") as audio:
                    # Prepare transcription parameters
                    # Note: Groq Whisper auto-detects language, so we don't force it
                    # This allows better multilingual support
                    transcription_params = {
                        "file": (filename, audio),
                        "model": self.model,
                        "response_format": "verbose_json",
                    }
                    
                    # Call Groq Whisper API
                    transcription = self.client.audio.transcriptions.create(**transcription_params)
                    
                    # Extract text and detected language
                    text = transcription.text
                    detected_language = getattr(transcription, 'language', language or 'en')
                    
                    return {
                        "text": text,
                        "language": detected_language
                    }
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    def is_supported_language(self, language_code: str) -> bool:
        """Check if a language is supported."""
        return language_code in settings.SUPPORTED_LANGUAGES

