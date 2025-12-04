"""
Emergency Message Service

Handles sending emergency alerts via WhatsApp and SMS.
Uses Twilio API for message delivery.
"""

import os
from typing import List, Optional
from datetime import datetime
import logging

from app.models.emergency_schemas import (
    EmergencyAlert,
    EmergencyContact,
    MessageDeliveryStatus,
    EmergencyResponse,
    LocationData,
    CrisisContext
)

logger = logging.getLogger(__name__)


class EmergencyMessageService:
    """Service for sending emergency messages via WhatsApp and SMS."""
    
    def __init__(self):
        """Initialize message service with Twilio credentials."""
        # Twilio credentials from environment
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_from = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # Twilio sandbox
        self.sms_from = os.getenv("TWILIO_PHONE_NUMBER")
        
        # Check if Twilio is configured
        self.twilio_enabled = bool(self.account_sid and self.auth_token)
        
        if self.twilio_enabled:
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.twilio_enabled = False
                self.client = None
        else:
            self.client = None
            logger.warning("Twilio not configured - emergency messages will be simulated")
    
    def _build_emergency_message(
        self,
        contact_name: str,
        user_name: Optional[str],
        location: LocationData,
        crisis_context: Optional[CrisisContext]
    ) -> str:
        """
        Build emergency message text.
        
        Args:
            contact_name: Name of the emergency contact
            user_name: Name of the user in crisis (if provided)
            location: User's location data
            crisis_context: Crisis context information
            
        Returns:
            Formatted emergency message
        """
        user_display = user_name if user_name else "Your contact"
        
        # Start with urgent header
        message = f"🚨 URGENT: {user_display} needs help!\n\n"
        
        # Add crisis context if available
        if crisis_context:
            if crisis_context.detected_emotion:
                message += f"Mental State: {crisis_context.detected_emotion.title()}\n"
            
            if crisis_context.crisis_indicators:
                indicators = ", ".join(crisis_context.crisis_indicators[:3])  # Limit to 3
                message += f"Concerns: {indicators}\n"
            
            if crisis_context.recent_concerns:
                # Truncate to 100 chars
                concerns = crisis_context.recent_concerns[:100]
                if len(crisis_context.recent_concerns) > 100:
                    concerns += "..."
                message += f"Recent: {concerns}\n"
            
            message += "\n"
        
        # Add location
        message += "📍 Location:\n"
        message += f"{location.get_display_text()}\n"
        
        maps_link = location.get_google_maps_link()
        if maps_link:
            message += f"{maps_link}\n"
        
        message += "\n"
        
        # Add crisis resources
        message += "🆘 Immediate Help:\n"
        message += "• AASRA: 9820466726\n"
        message += "• Vandrevala: 1860-2662-345\n"
        message += "• iCall: 9152987821\n"
        message += "• NIMHANS: 080-46110007\n\n"
        
        message += "Please reach out to them immediately. They may need your support right now."
        
        return message
    
    def _send_whatsapp(
        self,
        to_number: str,
        message: str
    ) -> tuple[bool, Optional[str]]:
        """
        Send WhatsApp message via Twilio.
        
        Args:
            to_number: Recipient phone number with country code
            message: Message text
            
        Returns:
            Tuple of (success, error_message)
        """
        if not self.twilio_enabled:
            logger.info(f"[SIMULATED] WhatsApp to {to_number}: {message[:50]}...")
            return True, None
        
        try:
            # Format WhatsApp number
            whatsapp_to = f"whatsapp:{to_number}"
            
            message_obj = self.client.messages.create(
                from_=self.whatsapp_from,
                to=whatsapp_to,
                body=message
            )
            
            logger.info(f"WhatsApp sent successfully to {to_number}, SID: {message_obj.sid}")
            return True, None
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to send WhatsApp to {to_number}: {error_msg}")
            return False, error_msg
    
    def _send_sms(
        self,
        to_number: str,
        message: str
    ) -> tuple[bool, Optional[str]]:
        """
        Send SMS message via Twilio.
        
        Args:
            to_number: Recipient phone number with country code
            message: Message text
            
        Returns:
            Tuple of (success, error_message)
        """
        if not self.twilio_enabled:
            logger.info(f"[SIMULATED] SMS to {to_number}: {message[:50]}...")
            return True, None
        
        if not self.sms_from:
            logger.warning(f"SMS phone number not configured, skipping SMS to {to_number}")
            return False, "SMS phone number not configured (optional)"
        
        # Check if SMS number is the WhatsApp number (common mistake)
        if self.sms_from == self.whatsapp_from or 'whatsapp:' in self.sms_from:
            logger.warning(f"SMS number appears to be WhatsApp number, skipping SMS to {to_number}")
            return False, "SMS number is WhatsApp number (configure separate SMS number)"
        
        try:
            message_obj = self.client.messages.create(
                from_=self.sms_from,
                to=to_number,
                body=message
            )
            
            logger.info(f"SMS sent successfully to {to_number}, SID: {message_obj.sid}")
            return True, None
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to send SMS to {to_number}: {error_msg}")
            return False, error_msg
    
    def send_emergency_alerts(
        self,
        contacts: List[EmergencyContact],
        alert: EmergencyAlert
    ) -> EmergencyResponse:
        """
        Send emergency alerts to all contacts.
        
        Args:
            contacts: List of emergency contacts
            alert: Emergency alert data
            
        Returns:
            EmergencyResponse with delivery status
        """
        delivery_statuses = []
        successful_alerts = 0
        
        # Build message once
        message = self._build_emergency_message(
            contact_name="",  # Will be personalized per contact
            user_name=alert.user_name,
            location=alert.location,
            crisis_context=alert.crisis_context
        )
        
        # Add test mode indicator
        if alert.is_test:
            message = "🧪 TEST ALERT - This is a test message\n\n" + message
        
        # Send to each contact
        for contact in contacts:
            status = MessageDeliveryStatus(
                contact_name=contact.name,
                phone=contact.phone
            )
            
            # Personalize message
            personalized_msg = message.replace(
                "📍 Location:",
                f"Hi {contact.name},\n\n📍 Location:"
            )
            
            # Send WhatsApp if enabled
            if contact.whatsapp_enabled:
                whatsapp_success, whatsapp_error = self._send_whatsapp(
                    contact.phone,
                    personalized_msg
                )
                status.whatsapp_sent = whatsapp_success
                status.whatsapp_error = whatsapp_error
            
            # Send SMS as backup (optional - only if configured)
            sms_success, sms_error = self._send_sms(
                contact.phone,
                personalized_msg
            )
            status.sms_sent = sms_success
            status.sms_error = sms_error
            
            # Mark as successful if either method worked
            # Note: SMS errors are non-critical if WhatsApp succeeded
            status.success = status.whatsapp_sent or status.sms_sent
            
            # Log success status
            if status.whatsapp_sent and not status.sms_sent:
                logger.info(f"Alert sent to {contact.name} via WhatsApp (SMS skipped: {sms_error})")
            elif status.sms_sent and not status.whatsapp_sent:
                logger.info(f"Alert sent to {contact.name} via SMS (WhatsApp failed: {whatsapp_error})")
            elif status.whatsapp_sent and status.sms_sent:
                logger.info(f"Alert sent to {contact.name} via both WhatsApp and SMS")
            else:
                logger.error(f"Failed to send alert to {contact.name} via any method")
            
            if status.success:
                successful_alerts += 1
            
            delivery_statuses.append(status)
        
        # Build response
        overall_success = successful_alerts > 0
        
        if overall_success:
            message = f"Emergency alerts sent to {successful_alerts}/{len(contacts)} contacts"
        else:
            message = "Failed to send emergency alerts to any contacts"
        
        return EmergencyResponse(
            success=overall_success,
            message=message,
            alerts_sent=successful_alerts,
            total_contacts=len(contacts),
            delivery_status=delivery_statuses,
            timestamp=datetime.now()
        )
    
    def send_test_message(
        self,
        contact: EmergencyContact,
        user_name: Optional[str] = None
    ) -> MessageDeliveryStatus:
        """
        Send a test message to a single contact.
        
        Args:
            contact: Emergency contact to test
            user_name: User's name (optional)
            
        Returns:
            MessageDeliveryStatus with delivery results
        """
        status = MessageDeliveryStatus(
            contact_name=contact.name,
            phone=contact.phone
        )
        
        # Build test message
        user_display = user_name if user_name else "Your contact"
        message = (
            f"🧪 TEST MESSAGE\n\n"
            f"Hi {contact.name},\n\n"
            f"This is a test of the emergency contact system for {user_display}. "
            f"If this were a real emergency, you would receive their location and crisis information.\n\n"
            f"You are successfully set up as an emergency contact. ✅\n\n"
            f"Crisis Helplines:\n"
            f"• AASRA: 9820466726\n"
            f"• Vandrevala: 1860-2662-345"
        )
        
        # Send WhatsApp if enabled
        if contact.whatsapp_enabled:
            whatsapp_success, whatsapp_error = self._send_whatsapp(
                contact.phone,
                message
            )
            status.whatsapp_sent = whatsapp_success
            status.whatsapp_error = whatsapp_error
        
        # Send SMS
        sms_success, sms_error = self._send_sms(
            contact.phone,
            message
        )
        status.sms_sent = sms_success
        status.sms_error = sms_error
        
        # Mark as successful if either method worked
        status.success = status.whatsapp_sent or status.sms_sent
        
        return status


# Singleton instance
_message_service = None


def get_message_service() -> EmergencyMessageService:
    """Get or create singleton message service instance."""
    global _message_service
    if _message_service is None:
        _message_service = EmergencyMessageService()
    return _message_service

