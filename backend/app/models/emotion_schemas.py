from typing import Optional, List
from pydantic import BaseModel, Field


class EmotionAnalysis(BaseModel):
    """Emotion analysis result from LLM."""
    primary_emotion: str = Field(..., description="Main detected emotion")
    intensity: float = Field(..., ge=0.0, le=1.0, description="Emotion intensity (0.0 to 1.0)")
    secondary_emotion: Optional[str] = Field(None, description="Secondary emotion if present")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence (0.0 to 1.0)")
    recommended_style: str = Field(..., description="Recommended voice style")
    recommended_pace: str = Field(..., description="Recommended speech pace")
    key_concerns: List[str] = Field(default_factory=list, description="Extracted key topics/concerns")
    crisis_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Crisis severity (0.0 to 1.0)")


class VoiceParameters(BaseModel):
    """Voice synthesis parameters based on emotion."""
    style: str = Field(default="friendly", description="Voice style/emotion")
    rate: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech rate multiplier")
    pitch: str = Field(default="0%", description="Pitch adjustment")
    volume: str = Field(default="medium", description="Volume level")
    pause_duration: int = Field(default=300, description="Pause duration in milliseconds")
    emphasis_level: str = Field(default="moderate", description="Emphasis level for key words")

