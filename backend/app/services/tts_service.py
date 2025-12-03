import base64
import tempfile
import os
from typing import Optional
import edge_tts
from ..config import settings
from ..models.emotion_schemas import VoiceParameters
from ..utils.ssml_builder import SSMLBuilder


class TTSService:
    """Text-to-Speech service using Edge TTS."""
    
    def __init__(self):
        """Initialize the TTS service."""
        self.voices = settings.SUPPORTED_LANGUAGES
        self.ssml_builder = SSMLBuilder()
    
    async def text_to_speech(
        self, 
        text: str, 
        language: str = "en",
        voice_params: Optional[VoiceParameters] = None,
        use_ssml: bool = True
    ) -> str:
        """
        Convert text to speech and return as base64 encoded audio.
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'hi')
            voice_params: Optional voice parameters for emotional speech
            use_ssml: Whether to use SSML for natural speech
            
        Returns:
            Base64 encoded audio data
        """
        # List of voices to try for each language (primary + fallbacks)
        voice_options = {
            "hi": ["hi-IN-SwaraNeural", "hi-IN-MadhurNeural"],
            "en": ["en-US-AriaNeural", "en-US-JennyNeural"],
            "es": ["es-ES-ElviraNeural", "es-MX-DaliaNeural"],
            "fr": ["fr-FR-DeniseNeural", "fr-CA-SylvieNeural"],
            "de": ["de-DE-KatjaNeural", "de-DE-ConradNeural"],
            "pt": ["pt-BR-FranciscaNeural", "pt-PT-RaquelNeural"],
            "it": ["it-IT-ElsaNeural", "it-IT-DiegoNeural"],
            "ja": ["ja-JP-NanamiNeural", "ja-JP-KeitaNeural"],
            "ko": ["ko-KR-SunHiNeural", "ko-KR-InJoonNeural"],
            "zh": ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural"],
        }
        
        # Get voices to try for this language
        voices_to_try = voice_options.get(language, ["en-US-AriaNeural"])
        
        # Use default voice parameters if not provided
        if voice_params is None:
            voice_params = VoiceParameters()
        
        last_error = None
        for voice in voices_to_try:
            try:
                print(f"Trying voice: {voice} for language: {language}")
                
                # Prepare text for TTS - use plain text (SSML not supported by edge-tts library)
                tts_text = text
                
                # Calculate rate adjustment for Edge TTS (supports rate as string like "+20%" or "-10%")
                if voice_params:
                    # Convert rate multiplier to percentage
                    rate_percent = int((voice_params.rate - 1.0) * 100)
                    rate_str = f"{rate_percent:+d}%" if rate_percent != 0 else "+0%"
                    
                    # Convert pitch - Edge TTS expects format like "+5Hz" or "-10Hz", not percentages
                    # Extract the number from pitch string (e.g., "-3%" -> -3)
                    try:
                        pitch_value = int(voice_params.pitch.replace("%", ""))
                        # Convert percentage to Hz (rough approximation: 1% ≈ 5Hz)
                        pitch_hz = pitch_value * 5
                        pitch_str = f"{pitch_hz:+d}Hz" if pitch_hz != 0 else "+0Hz"
                    except:
                        pitch_str = "+0Hz"
                    
                    # Convert volume to percentage
                    volume_map = {"soft": "-20%", "medium": "+0%", "loud": "+20%"}
                    volume_str = volume_map.get(voice_params.volume, "+0%")
                    
                    print(f"Using emotional voice: style={voice_params.style}, rate={rate_str}, pitch={pitch_str}, volume={volume_str}")
                else:
                    rate_str = "+0%"
                    pitch_str = "+0Hz"
                    volume_str = "+0%"
                
                # Create a temporary file for the audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file_path = temp_file.name
                
                try:
                    # Generate speech using Edge TTS with prosody parameters
                    communicate = edge_tts.Communicate(
                        tts_text, 
                        voice,
                        rate=rate_str,
                        pitch=pitch_str,
                        volume=volume_str
                    )
                    await communicate.save(temp_file_path)
                    
                    # Read the audio file and encode to base64
                    with open(temp_file_path, "rb") as audio_file:
                        audio_data = audio_file.read()
                        
                        # Check if we actually got audio data
                        if len(audio_data) == 0:
                            raise Exception("No audio data generated")
                        
                        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    
                    print(f"Successfully generated speech with voice: {voice}")
                    return audio_base64
                    
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                        
            except Exception as e:
                print(f"Failed with voice {voice}: {str(e)}")
                last_error = e
                continue  # Try next voice
        
        # If all voices failed, raise the last error
        raise Exception(f"Error generating speech after trying all voices: {str(last_error)}")
    
    def get_available_voices(self) -> dict:
        """
        Get all available voices for supported languages.
        
        Returns:
            Dictionary of language codes to voice information
        """
        return self.voices
    
    def is_supported_language(self, language_code: str) -> bool:
        """Check if a language is supported for TTS."""
        return language_code in self.voices

