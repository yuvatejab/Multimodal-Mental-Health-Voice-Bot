from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import re


class EmergencyContact(BaseModel):
    """Model for emergency contact information."""
    name: str = Field(..., min_length=1, max_length=100, description="Contact's full name")
    phone: str = Field(..., description="Phone number with country code (e.g., +919876543210)")
    relationship: str = Field(..., description="Relationship to user (Family, Friend, Partner, Therapist, Other)")
    whatsapp_enabled: bool = Field(default=True, description="Whether to send WhatsApp messages")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format."""
        # Remove spaces and dashes
        phone = re.sub(r'[\s\-]', '', v)
        
        # Check if it starts with + and has 10-15 digits
        if not re.match(r'^\+\d{10,15}$', phone):
            raise ValueError('Phone number must start with + and country code (e.g., +919876543210)')
        
        return phone
    
    @validator('relationship')
    def validate_relationship(cls, v):
        """Validate relationship is from allowed list."""
        allowed = ['Family', 'Friend', 'Partner', 'Therapist', 'Other']
        if v not in allowed:
            raise ValueError(f'Relationship must be one of: {", ".join(allowed)}')
        return v


class EmergencyContactList(BaseModel):
    """Model for list of emergency contacts."""
    session_id: str = Field(..., description="User session ID")
    contacts: List[EmergencyContact] = Field(..., min_items=1, max_items=3, description="1-3 emergency contacts")
    location_permission: bool = Field(default=False, description="Whether user granted location permission")
    setup_completed: bool = Field(default=True, description="Whether setup is complete")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class LocationData(BaseModel):
    """Model for user location data."""
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    accuracy: Optional[float] = Field(None, description="Accuracy in meters")
    address: Optional[str] = Field(None, description="Manual address if geolocation unavailable")
    
    def get_google_maps_link(self) -> Optional[str]:
        """Generate Google Maps link from coordinates."""
        if self.latitude and self.longitude:
            return f"https://maps.google.com/?q={self.latitude},{self.longitude}"
        return None
    
    def get_display_text(self) -> str:
        """Get human-readable location text."""
        if self.latitude and self.longitude:
            accuracy_text = f" (±{int(self.accuracy)}m)" if self.accuracy else ""
            return f"Lat: {self.latitude:.6f}, Lng: {self.longitude:.6f}{accuracy_text}"
        elif self.address:
            return self.address
        return "Location unavailable"


class CrisisContext(BaseModel):
    """Model for crisis context information."""
    detected_emotion: Optional[str] = Field(None, description="Detected emotion (anxiety, depression, etc.)")
    crisis_indicators: List[str] = Field(default_factory=list, description="List of crisis keywords detected")
    recent_concerns: Optional[str] = Field(None, description="Summary of recent conversation concerns")
    intensity: Optional[float] = Field(None, ge=0.0, le=1.0, description="Crisis intensity (0-1)")
    timestamp: datetime = Field(default_factory=datetime.now)


class EmergencyAlert(BaseModel):
    """Model for emergency alert request."""
    session_id: str = Field(..., description="User session ID")
    location: LocationData = Field(..., description="User location data")
    crisis_context: Optional[CrisisContext] = Field(None, description="Crisis context from conversation")
    user_name: Optional[str] = Field(None, description="User's name (if provided)")
    is_test: bool = Field(default=False, description="Whether this is a test alert")


class MessageDeliveryStatus(BaseModel):
    """Model for individual message delivery status."""
    contact_name: str
    phone: str
    whatsapp_sent: bool = False
    whatsapp_error: Optional[str] = None
    sms_sent: bool = False
    sms_error: Optional[str] = None
    success: bool = False


class EmergencyResponse(BaseModel):
    """Model for emergency alert response."""
    success: bool = Field(..., description="Overall success status")
    message: str = Field(..., description="Response message")
    alerts_sent: int = Field(default=0, description="Number of successful alerts")
    total_contacts: int = Field(..., description="Total number of contacts")
    delivery_status: List[MessageDeliveryStatus] = Field(default_factory=list, description="Detailed delivery status")
    timestamp: datetime = Field(default_factory=datetime.now)


class TestMessageRequest(BaseModel):
    """Model for test message request."""
    session_id: str = Field(..., description="User session ID")
    contact_index: int = Field(..., ge=0, description="Index of contact to test (0-based)")

