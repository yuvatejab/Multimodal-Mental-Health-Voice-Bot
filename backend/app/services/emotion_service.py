import json
from typing import Optional, Dict
from groq import Groq
from ..config import settings
from ..models.emotion_schemas import EmotionAnalysis, VoiceParameters


class EmotionService:
    """Service for detecting emotions in user messages and mapping to voice parameters."""
    
    def __init__(self):
        """Initialize the emotion service with Groq client."""
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL
        
        # Cache for emotion analysis (session-based)
        self._emotion_cache: Dict[str, EmotionAnalysis] = {}
    
    async def analyze_emotion(self, user_message: str, use_cache: bool = True) -> EmotionAnalysis:
        """
        Analyze the emotional content of a user message.
        
        Args:
            user_message: The user's text message
            use_cache: Whether to use cached results
            
        Returns:
            EmotionAnalysis object with detected emotions and recommendations
        """
        # Check cache
        if use_cache and user_message in self._emotion_cache:
            return self._emotion_cache[user_message]
        
        try:
            # Prompt for emotion analysis
            analysis_prompt = f"""Analyze the emotional state in this message and respond with ONLY valid JSON (no markdown, no explanation):

Message: "{user_message}"

Return this exact JSON structure:
{{
  "primary_emotion": "<one of: anxious, sad, angry, happy, neutral, stressed, depressed, fearful, hopeful>",
  "intensity": <0.0 to 1.0>,
  "secondary_emotion": "<optional: same options as primary>",
  "confidence": <0.0 to 1.0>,
  "recommended_style": "<one of: empathetic, gentle, cheerful, calm, supportive, friendly>",
  "recommended_pace": "<one of: slow, normal, fast>",
  "key_concerns": ["<topic1>", "<topic2>"],
  "crisis_level": <0.0 to 1.0>
}}"""

            # Call Groq API
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an emotion analysis expert. Respond ONLY with valid JSON, no markdown formatting."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=300,
            )
            
            # Parse response
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            emotion_data = json.loads(response_text)
            
            # Create EmotionAnalysis object
            emotion_analysis = EmotionAnalysis(**emotion_data)
            
            # Cache the result
            if use_cache:
                self._emotion_cache[user_message] = emotion_analysis
            
            return emotion_analysis
            
        except json.JSONDecodeError as e:
            print(f"Error parsing emotion JSON: {e}")
            print(f"Response was: {response_text}")
            # Return neutral fallback
            return self._get_neutral_emotion()
        except Exception as e:
            print(f"Error analyzing emotion: {str(e)}")
            # Return neutral fallback
            return self._get_neutral_emotion()
    
    def emotion_to_voice_parameters(self, emotion: EmotionAnalysis) -> VoiceParameters:
        """
        Convert emotion analysis to voice synthesis parameters.
        
        Args:
            emotion: EmotionAnalysis object
            
        Returns:
            VoiceParameters for TTS
        """
        # Emotion-to-parameter mapping (subtle adjustments for natural speech)
        emotion_map = {
            "anxious": {
                "style": "empathetic",
                "rate": 0.95,  # Very subtle slowdown (5% slower)
                "pitch": "-1%",  # Slight lower pitch
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "sad": {
                "style": "empathetic",
                "rate": 0.97,  # Barely slower (3% slower)
                "pitch": "-1%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "depressed": {
                "style": "empathetic",
                "rate": 0.95,
                "pitch": "-1%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "angry": {
                "style": "calm",
                "rate": 0.95,  # Slightly slower to sound calmer
                "pitch": "-1%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "stressed": {
                "style": "supportive",
                "rate": 0.97,  # Just a touch slower
                "pitch": "-1%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "fearful": {
                "style": "gentle",
                "rate": 0.97,
                "pitch": "0%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "happy": {
                "style": "cheerful",
                "rate": 1.03,  # Slightly faster (3% faster)
                "pitch": "+1%",
                "volume": "medium",
                "pause_duration": 250,
                "emphasis_level": "moderate"
            },
            "hopeful": {
                "style": "friendly",
                "rate": 1.0,  # Normal speed
                "pitch": "0%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            },
            "neutral": {
                "style": "friendly",
                "rate": 1.0,  # Normal speed
                "pitch": "0%",
                "volume": "medium",
                "pause_duration": 300,
                "emphasis_level": "moderate"
            }
        }
        
        # Get base parameters for primary emotion
        base_params = emotion_map.get(
            emotion.primary_emotion.lower(),
            emotion_map["neutral"]
        )
        
        # Adjust based on intensity
        adjusted_params = base_params.copy()
        
        # Higher intensity = more pronounced adjustments
        if emotion.intensity > 0.7:
            # Amplify the effect
            if adjusted_params["rate"] < 1.0:
                adjusted_params["rate"] = max(0.75, adjusted_params["rate"] - 0.05)
            adjusted_params["pause_duration"] = int(adjusted_params["pause_duration"] * 1.2)
        elif emotion.intensity < 0.3:
            # Moderate the effect
            adjusted_params["rate"] = min(1.0, adjusted_params["rate"] + 0.05)
            adjusted_params["pause_duration"] = int(adjusted_params["pause_duration"] * 0.8)
        
        return VoiceParameters(**adjusted_params)
    
    def _get_neutral_emotion(self) -> EmotionAnalysis:
        """Return a neutral emotion analysis as fallback."""
        return EmotionAnalysis(
            primary_emotion="neutral",
            intensity=0.5,
            confidence=0.5,
            recommended_style="friendly",
            recommended_pace="normal",
            key_concerns=[],
            crisis_level=0.0
        )
    
    def clear_cache(self):
        """Clear the emotion analysis cache."""
        self._emotion_cache.clear()

