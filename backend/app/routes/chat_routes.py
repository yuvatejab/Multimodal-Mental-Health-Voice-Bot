from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
from ..models.schemas import (
    ChatRequest,
    ChatResponse,
    VoiceChatResponse,
    LanguageInfo,
    ErrorResponse,
    TranscriptionResponse
)
from ..services.therapy_service import TherapyService
from ..config import settings

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize therapy service
therapy_service = TherapyService()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Mental Health Voice Bot API is running"}


@router.get("/languages", response_model=list[LanguageInfo])
async def get_supported_languages():
    """
    Get list of supported languages.
    
    Returns:
        List of supported languages with their details
    """
    languages = []
    for code, info in settings.SUPPORTED_LANGUAGES.items():
        languages.append(
            LanguageInfo(
                code=code,
                name=info["name"],
                voice=info["voice"]
            )
        )
    return languages


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(default="en")
):
    """
    Transcribe audio to text.
    
    Args:
        audio: Audio file (webm, mp3, wav, etc.)
        language: Optional language code
        
    Returns:
        Transcribed text and detected language
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()
        
        # Validate file size
        if len(audio_bytes) > settings.MAX_AUDIO_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Audio file too large. Maximum size: {settings.MAX_AUDIO_SIZE_MB}MB"
            )
        
        # Transcribe
        result = await therapy_service.stt_service.transcribe_audio(
            audio_file=audio_bytes,
            language=language,
            filename=audio.filename or "audio.webm"
        )
        
        return TranscriptionResponse(
            text=result["text"],
            language=result["language"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transcribing audio: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def text_chat(request: ChatRequest):
    """
    Text-based chat endpoint.
    
    Args:
        request: Chat request with message and optional context
        
    Returns:
        Bot's text response
    """
    try:
        # Process message
        result = await therapy_service.process_message(
            message=request.message,
            session_id=None,  # Create new session each time for stateless API
            language=request.language
        )
        
        return ChatResponse(
            response=result["response"],
            language=result["language"],
            is_crisis=result["is_crisis"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )


@router.post("/voice-chat", response_model=VoiceChatResponse)
async def voice_chat(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(default=None),
    session_id: Optional[str] = Form(default=None)
):
    """
    Complete voice chat pipeline: STT -> LLM -> TTS.
    
    Args:
        audio: Audio file with user's voice message
        language: Optional language code
        session_id: Optional session ID for conversation context
        
    Returns:
        Transcription, text response, and audio response
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()
        
        # Validate file size
        if len(audio_bytes) > settings.MAX_AUDIO_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Audio file too large. Maximum size: {settings.MAX_AUDIO_SIZE_MB}MB"
            )
        
        # Process voice message through complete pipeline
        result = await therapy_service.process_voice_message(
            audio_file=audio_bytes,
            filename=audio.filename or "audio.webm",
            session_id=session_id,
            language=language
        )
        
        return VoiceChatResponse(
            transcription=result["transcription"],
            response=result["response"],
            audio_base64=result["audio_base64"],
            language=result["language"],
            is_crisis=result["is_crisis"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error in voice chat: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing voice chat: {str(e)}"
        )


@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    """
    Get conversation history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Conversation history
    """
    try:
        history = therapy_service.get_conversation_history(session_id)
        return {"session_id": session_id, "history": history}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving session history: {str(e)}"
        )


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """
    Clear a session and its conversation history.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Success message
    """
    try:
        therapy_service.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing session: {str(e)}"
        )

