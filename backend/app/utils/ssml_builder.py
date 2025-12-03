import re
from typing import List, Tuple
from ..models.emotion_schemas import VoiceParameters


class SSMLBuilder:
    """Build SSML (Speech Synthesis Markup Language) for natural, emotional speech."""
    
    # Emotional keywords that should be emphasized
    EMPHASIS_KEYWORDS = {
        "support": ["understand", "here for you", "support", "help", "listen", "care"],
        "validation": ["valid", "normal", "okay", "natural", "common", "understandable"],
        "empathy": ["feel", "difficult", "challenging", "hard", "tough", "struggle"],
        "hope": ["better", "improve", "progress", "hope", "positive", "forward"],
    }
    
    # Words that should have pauses after them
    PAUSE_AFTER = ["however", "but", "and", "also", "additionally", "furthermore"]
    
    def __init__(self):
        """Initialize the SSML builder."""
        pass
    
    def build_ssml(
        self,
        text: str,
        voice_name: str,
        voice_params: VoiceParameters,
        language: str = "en"
    ) -> str:
        """
        Build complete SSML from text and voice parameters.
        
        Args:
            text: The text to convert to speech
            voice_name: The Edge TTS voice name
            voice_params: Voice parameters (style, rate, pitch, etc.)
            language: Language code
            
        Returns:
            Complete SSML string
        """
        # Escape any XML special characters in the original text
        escaped_text = self.escape_ssml(text)
        
        # Process text: add pauses and emphasis
        processed_text = self._add_natural_pauses(escaped_text, voice_params.pause_duration)
        processed_text = self._add_emphasis(processed_text, voice_params.emphasis_level)
        
        # Check if voice supports emotional styles (only some neural voices do)
        supports_styles = self._voice_supports_styles(voice_name)
        
        if supports_styles:
            # Build SSML with emotional style
            ssml = self._build_with_style(
                processed_text,
                voice_name,
                voice_params,
                language
            )
        else:
            # Build SSML with prosody only (no style)
            ssml = self._build_with_prosody(
                processed_text,
                voice_name,
                voice_params,
                language
            )
        
        return ssml
    
    def _build_with_style(
        self,
        text: str,
        voice_name: str,
        voice_params: VoiceParameters,
        language: str
    ) -> str:
        """Build SSML with emotional style support."""
        # Map our styles to Edge TTS styles
        style_map = {
            "empathetic": "empathetic",
            "gentle": "gentle",
            "cheerful": "cheerful",
            "calm": "calm",
            "supportive": "friendly",
            "friendly": "friendly"
        }
        
        edge_style = style_map.get(voice_params.style, "friendly")
        
        # Simplified SSML - just use prosody without complex nesting
        # Edge TTS sometimes has issues with complex SSML
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self._get_xml_lang(language)}">
<voice name="{voice_name}">
<prosody rate="{voice_params.rate}" pitch="{voice_params.pitch}" volume="{voice_params.volume}">
{text}
</prosody>
</voice>
</speak>"""
        
        return ssml
    
    def _build_with_prosody(
        self,
        text: str,
        voice_name: str,
        voice_params: VoiceParameters,
        language: str
    ) -> str:
        """Build SSML with prosody only (for voices that don't support styles)."""
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self._get_xml_lang(language)}">
<voice name="{voice_name}">
<prosody rate="{voice_params.rate}" pitch="{voice_params.pitch}" volume="{voice_params.volume}">
{text}
</prosody>
</voice>
</speak>"""
        
        return ssml
    
    def _add_natural_pauses(self, text: str, base_pause_ms: int) -> str:
        """
        Add natural pauses at punctuation and key words.
        
        Args:
            text: Original text
            base_pause_ms: Base pause duration in milliseconds
            
        Returns:
            Text with SSML break tags
        """
        # Add pauses after sentences
        text = re.sub(r'\.(\s+)', f'.<break time="{base_pause_ms}ms"/>\\1', text)
        text = re.sub(r'\!(\s+)', f'!<break time="{base_pause_ms}ms"/>\\1', text)
        text = re.sub(r'\?(\s+)', f'?<break time="{base_pause_ms}ms"/>\\1', text)
        
        # Add shorter pauses after commas
        comma_pause = int(base_pause_ms * 0.6)
        text = re.sub(r',(\s+)', f',<break time="{comma_pause}ms"/>\\1', text)
        
        # Add pauses after specific words
        for word in self.PAUSE_AFTER:
            pattern = rf'\b{word}\b(\s+)'
            replacement = f'{word}<break time="{int(base_pause_ms * 0.5)}ms"/>\\1'
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_emphasis(self, text: str, emphasis_level: str) -> str:
        """
        Add emphasis to emotional keywords.
        
        Args:
            text: Original text
            emphasis_level: Level of emphasis (reduced, moderate, strong)
            
        Returns:
            Text with SSML emphasis tags
        """
        if emphasis_level == "reduced":
            return text  # No emphasis for calm/reduced style
        
        # Collect all keywords to emphasize
        all_keywords = []
        for category_keywords in self.EMPHASIS_KEYWORDS.values():
            all_keywords.extend(category_keywords)
        
        # Add emphasis tags
        for keyword in all_keywords:
            # Match whole words only
            pattern = rf'\b({re.escape(keyword)})\b'
            replacement = f'<emphasis level="{emphasis_level}">\\1</emphasis>'
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _voice_supports_styles(self, voice_name: str) -> bool:
        """
        Check if a voice supports emotional styles.
        
        Args:
            voice_name: Edge TTS voice name
            
        Returns:
            True if voice supports styles
        """
        # Neural voices that support styles
        style_supported_voices = [
            "en-US-AriaNeural",
            "en-US-JennyNeural",
            "en-US-GuyNeural",
            "en-GB-SoniaNeural",
            "zh-CN-XiaoxiaoNeural",
            "zh-CN-YunxiNeural",
        ]
        
        return voice_name in style_supported_voices
    
    def _get_xml_lang(self, language_code: str) -> str:
        """
        Convert language code to XML lang format.
        
        Args:
            language_code: Language code (e.g., 'en', 'hi')
            
        Returns:
            XML lang string (e.g., 'en-US', 'hi-IN')
        """
        lang_map = {
            "en": "en-US",
            "hi": "hi-IN",
            "es": "es-ES",
            "fr": "fr-FR",
            "de": "de-DE",
            "pt": "pt-BR",
            "it": "it-IT",
            "ja": "ja-JP",
            "ko": "ko-KR",
            "zh": "zh-CN",
        }
        
        return lang_map.get(language_code, "en-US")
    
    def escape_ssml(self, text: str) -> str:
        """
        Escape special XML characters in text.
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text safe for SSML
        """
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        return text

