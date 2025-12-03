from typing import List, Dict, Optional
from datetime import datetime
from .llm_service import LLMService
from .stt_service import STTService
from .tts_service import TTSService
from .emotion_service import EmotionService


class TherapyService:
    """
    Orchestrates the mental health conversation flow.
    Manages conversation context, safety checks, and coordinates between services.
    """
    
    def __init__(self):
        """Initialize therapy service with required sub-services."""
        self.llm_service = LLMService()
        self.stt_service = STTService()
        self.tts_service = TTSService()
        self.emotion_service = EmotionService()
        
        # In-memory session storage (in production, use Redis or database)
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self, session_id: str) -> Dict:
        """
        Create a new therapy session.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session data dictionary
        """
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now(),
            "conversation_history": [],
            "language": "en",
            "crisis_detected": False
        }
        return self.sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve an existing session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found
        """
        return self.sessions.get(session_id)
    
    def update_session_language(self, session_id: str, language: str):
        """Update the language preference for a session."""
        if session_id in self.sessions:
            self.sessions[session_id]["language"] = language
    
    def add_to_conversation_history(
        self, 
        session_id: str, 
        role: str, 
        content: str
    ):
        """
        Add a message to the conversation history.
        
        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        if session_id in self.sessions:
            self.sessions[session_id]["conversation_history"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 20 messages to manage memory
            if len(self.sessions[session_id]["conversation_history"]) > 20:
                self.sessions[session_id]["conversation_history"] = \
                    self.sessions[session_id]["conversation_history"][-20:]
    
    async def process_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        language: str = "en"
    ) -> Dict:
        """
        Process a text message and generate a response.
        
        Args:
            message: User's text message
            session_id: Optional session ID for context
            language: Language code
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Create session if it doesn't exist
            if not session_id or session_id not in self.sessions:
                session_id = f"session_{datetime.now().timestamp()}"
                self.create_session(session_id)
            
            session = self.get_session(session_id)
            
            # Update language preference
            self.update_session_language(session_id, language)
            
            # Check for crisis indicators
            is_crisis = await self.llm_service.detect_crisis(message)
            
            if is_crisis:
                session["crisis_detected"] = True
                response = await self.llm_service.get_crisis_response(language)
            else:
                # Get conversation history for context
                history = session.get("conversation_history", [])
                
                # Generate response using LLM
                response = await self.llm_service.generate_response(
                    user_message=message,
                    conversation_history=history,
                    language=language
                )
            
            # Add to conversation history
            self.add_to_conversation_history(session_id, "user", message)
            self.add_to_conversation_history(session_id, "assistant", response)
            
            return {
                "response": response,
                "session_id": session_id,
                "is_crisis": is_crisis,
                "language": language
            }
            
        except Exception as e:
            raise Exception(f"Error processing message: {str(e)}")
    
    async def process_voice_message(
        self,
        audio_file: bytes,
        filename: str,
        session_id: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict:
        """
        Process a voice message through the complete pipeline:
        Speech-to-Text -> LLM -> Text-to-Speech
        
        Args:
            audio_file: Audio file bytes
            filename: Original filename
            session_id: Optional session ID for context
            language: Optional language code
            
        Returns:
            Dictionary with transcription, response, and audio
        """
        try:
            # Step 1: Transcribe audio to text
            transcription_result = await self.stt_service.transcribe_audio(
                audio_file=audio_file,
                language=language,
                filename=filename
            )
            
            transcribed_text = transcription_result["text"]
            detected_language = transcription_result.get("language", language or "en")
            
            # Use the user-selected language if provided, otherwise use detected
            if language and language in ["en", "hi", "es", "fr", "de", "pt", "it", "ja", "ko", "zh"]:
                detected_language = language
            
            print(f"Transcribed: {transcribed_text}")
            print(f"User selected language: {language}")
            print(f"Final language for TTS: {detected_language}")
            
            # Step 2: Analyze emotion in user's message
            try:
                emotion_analysis = await self.emotion_service.analyze_emotion(transcribed_text)
                print(f"Detected emotion: {emotion_analysis.primary_emotion} (intensity: {emotion_analysis.intensity})")
                print(f"Recommended style: {emotion_analysis.recommended_style}")
            except Exception as e:
                print(f"Emotion analysis failed: {str(e)}, using neutral")
                emotion_analysis = None
            
            # Step 3: Process the message through therapy logic
            processing_result = await self.process_message(
                message=transcribed_text,
                session_id=session_id,
                language=detected_language
            )
            
            response_text = processing_result["response"]
            is_crisis = processing_result["is_crisis"]
            
            # Step 4: Convert emotion to voice parameters
            if emotion_analysis:
                voice_params = self.emotion_service.emotion_to_voice_parameters(emotion_analysis)
            else:
                voice_params = None
            
            # Step 5: Convert response to speech with emotional voice
            audio_base64 = await self.tts_service.text_to_speech(
                text=response_text,
                language=detected_language,
                voice_params=voice_params,
                use_ssml=True
            )
            
            # Prepare response with emotion data
            response_data = {
                "transcription": transcribed_text,
                "response": response_text,
                "audio_base64": audio_base64,
                "session_id": processing_result["session_id"],
                "is_crisis": is_crisis,
                "language": detected_language
            }
            
            # Add emotion data if available
            if emotion_analysis:
                response_data["emotion"] = {
                    "primary": emotion_analysis.primary_emotion,
                    "intensity": emotion_analysis.intensity,
                    "style_used": voice_params.style if voice_params else "neutral"
                }
            
            return response_data
            
        except Exception as e:
            raise Exception(f"Error processing voice message: {str(e)}")
    
    def clear_session(self, session_id: str):
        """Clear a session from memory."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get the conversation history for a session."""
        session = self.get_session(session_id)
        if session:
            return session.get("conversation_history", [])
        return []

