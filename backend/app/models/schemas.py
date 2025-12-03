from typing import Optional, List
from pydantic import BaseModel, Field


class TranscriptionRequest(BaseModel):
    """Request model for audio transcription."""
    language: Optional[str] = Field(default="en", description="Language code for transcription")


class TranscriptionResponse(BaseModel):
    """Response model for audio transcription."""
    text: str = Field(..., description="Transcribed text from audio")
    language: str = Field(..., description="Detected or specified language")


class ChatRequest(BaseModel):
    """Request model for text-based chat."""
    message: str = Field(..., description="User's text message")
    language: str = Field(default="en", description="Language code for response")
    conversation_history: Optional[List[dict]] = Field(default=None, description="Previous conversation context")


class ChatResponse(BaseModel):
    """Response model for text-based chat."""
    response: str = Field(..., description="Bot's text response")
    language: str = Field(..., description="Response language")
    is_crisis: bool = Field(default=False, description="Whether crisis was detected")


class VoiceChatResponse(BaseModel):
    """Response model for voice chat with audio."""
    transcription: str = Field(..., description="Transcribed user input")
    response: str = Field(..., description="Bot's text response")
    audio_base64: str = Field(..., description="Base64 encoded audio response")
    language: str = Field(..., description="Response language")
    is_crisis: bool = Field(default=False, description="Whether crisis was detected")


class LanguageInfo(BaseModel):
    """Information about a supported language."""
    code: str = Field(..., description="Language code (e.g., 'en', 'hi')")
    name: str = Field(..., description="Language name (e.g., 'English', 'Hindi')")
    voice: str = Field(..., description="TTS voice identifier")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")

