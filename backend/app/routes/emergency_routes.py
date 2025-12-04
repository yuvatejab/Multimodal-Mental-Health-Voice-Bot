"""
Emergency Contact API Routes

Endpoints for managing emergency contacts and sending alerts.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from app.models.emergency_schemas import (
    EmergencyContact,
    EmergencyContactList,
    EmergencyAlert,
    EmergencyResponse,
    TestMessageRequest,
    MessageDeliveryStatus
)
from app.services.emergency_storage import get_storage_service
from app.services.emergency_message_service import get_message_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/emergency", tags=["emergency"])


@router.post("/contacts/save", response_model=EmergencyContactList)
async def save_emergency_contacts(
    session_id: str,
    contacts: List[EmergencyContact],
    location_permission: bool = False
):
    """
    Save emergency contacts for a session.
    
    Args:
        session_id: User session ID
        contacts: List of 1-3 emergency contacts
        location_permission: Whether user granted location permission
        
    Returns:
        EmergencyContactList: Saved contact list
    """
    try:
        # Validate contact count
        if len(contacts) < 1 or len(contacts) > 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide 1-3 emergency contacts"
            )
        
        storage = get_storage_service()
        contact_list = storage.save_contacts(session_id, contacts, location_permission)
        
        logger.info(f"Saved {len(contacts)} emergency contacts for session {session_id}")
        
        return contact_list
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error saving emergency contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save emergency contacts"
        )


@router.get("/contacts/{session_id}", response_model=EmergencyContactList)
async def get_emergency_contacts(session_id: str):
    """
    Get emergency contacts for a session.
    
    Args:
        session_id: User session ID
        
    Returns:
        EmergencyContactList: Contact list
    """
    try:
        storage = get_storage_service()
        contact_list = storage.get_contacts(session_id)
        
        if not contact_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No emergency contacts found for this session"
            )
        
        return contact_list
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving emergency contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve emergency contacts"
        )


@router.put("/contacts/update", response_model=EmergencyContactList)
async def update_emergency_contacts(
    session_id: str,
    contacts: List[EmergencyContact],
    location_permission: bool = None
):
    """
    Update emergency contacts for a session.
    
    Args:
        session_id: User session ID
        contacts: Updated list of emergency contacts
        location_permission: Updated location permission (optional)
        
    Returns:
        EmergencyContactList: Updated contact list
    """
    try:
        # Validate contact count
        if len(contacts) < 1 or len(contacts) > 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide 1-3 emergency contacts"
            )
        
        storage = get_storage_service()
        contact_list = storage.update_contacts(session_id, contacts, location_permission)
        
        logger.info(f"Updated emergency contacts for session {session_id}")
        
        return contact_list
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating emergency contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update emergency contacts"
        )


@router.delete("/contacts/{session_id}")
async def delete_emergency_contacts(session_id: str):
    """
    Delete emergency contacts for a session.
    
    Args:
        session_id: User session ID
        
    Returns:
        Success message
    """
    try:
        storage = get_storage_service()
        deleted = storage.delete_contacts(session_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No emergency contacts found for this session"
            )
        
        logger.info(f"Deleted emergency contacts for session {session_id}")
        
        return {"message": "Emergency contacts deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting emergency contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete emergency contacts"
        )


@router.get("/contacts/check/{session_id}")
async def check_emergency_setup(session_id: str):
    """
    Check if emergency contacts are set up for a session.
    
    Args:
        session_id: User session ID
        
    Returns:
        Setup status
    """
    try:
        storage = get_storage_service()
        has_contacts = storage.has_contacts(session_id)
        contact_count = storage.get_contact_count(session_id)
        
        return {
            "setup_completed": has_contacts,
            "contact_count": contact_count,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error checking emergency setup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check emergency setup"
        )


@router.post("/alert/send", response_model=EmergencyResponse)
async def send_emergency_alert(alert: EmergencyAlert):
    """
    Send emergency alert to all contacts.
    
    Args:
        alert: Emergency alert data with location and crisis context
        
    Returns:
        EmergencyResponse: Delivery status for all contacts
    """
    try:
        # Get contacts for session
        storage = get_storage_service()
        contact_list = storage.get_contacts(alert.session_id)
        
        if not contact_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No emergency contacts found. Please set up contacts first."
            )
        
        # Send alerts
        message_service = get_message_service()
        response = message_service.send_emergency_alerts(
            contact_list.contacts,
            alert
        )
        
        logger.info(
            f"Emergency alert sent for session {alert.session_id}: "
            f"{response.alerts_sent}/{response.total_contacts} successful"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending emergency alert: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send emergency alert: {str(e)}"
        )


@router.post("/test/send", response_model=MessageDeliveryStatus)
async def send_test_message(request: TestMessageRequest):
    """
    Send a test message to a specific contact.
    
    Args:
        request: Test message request with session_id and contact_index
        
    Returns:
        MessageDeliveryStatus: Delivery status for the test message
    """
    try:
        # Get contacts for session
        storage = get_storage_service()
        contact_list = storage.get_contacts(request.session_id)
        
        if not contact_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No emergency contacts found"
            )
        
        # Validate contact index
        if request.contact_index < 0 or request.contact_index >= len(contact_list.contacts):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid contact index. Must be 0-{len(contact_list.contacts)-1}"
            )
        
        # Get specific contact
        contact = contact_list.contacts[request.contact_index]
        
        # Send test message
        message_service = get_message_service()
        status_result = message_service.send_test_message(contact)
        
        logger.info(
            f"Test message sent to {contact.name} ({contact.phone}): "
            f"WhatsApp={status_result.whatsapp_sent}, SMS={status_result.sms_sent}"
        )
        
        return status_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending test message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send test message: {str(e)}"
        )


@router.get("/health")
async def emergency_health_check():
    """
    Health check endpoint for emergency system.
    
    Returns:
        System status
    """
    try:
        storage = get_storage_service()
        message_service = get_message_service()
        
        return {
            "status": "healthy",
            "storage": "operational",
            "messaging": "operational" if message_service.twilio_enabled else "simulated",
            "twilio_configured": message_service.twilio_enabled
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

