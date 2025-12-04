"""
Emergency Contact Storage Service

Manages emergency contact storage and retrieval.
Uses in-memory storage for POC (can be upgraded to database later).
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from app.models.emergency_schemas import EmergencyContactList, EmergencyContact


class EmergencyStorageService:
    """Service for managing emergency contacts storage."""
    
    def __init__(self, storage_file: str = "backend/app/data/emergency_contacts.json"):
        """Initialize storage service with file path."""
        self.storage_file = storage_file
        self.storage_path = Path(storage_file)
        self._ensure_storage_exists()
        self._contacts_cache: Dict[str, EmergencyContactList] = {}
        self._load_from_file()
    
    def _ensure_storage_exists(self):
        """Ensure storage directory and file exist."""
        # Create directory if it doesn't exist
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create empty file if it doesn't exist
        if not self.storage_path.exists():
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)
    
    def _load_from_file(self):
        """Load contacts from file into cache."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for session_id, contact_data in data.items():
                    self._contacts_cache[session_id] = EmergencyContactList(**contact_data)
        except Exception as e:
            print(f"Error loading emergency contacts: {e}")
            self._contacts_cache = {}
    
    def _save_to_file(self):
        """Save contacts from cache to file."""
        try:
            data = {}
            for session_id, contact_list in self._contacts_cache.items():
                data[session_id] = contact_list.dict()
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving emergency contacts: {e}")
    
    def save_contacts(self, session_id: str, contacts: List[EmergencyContact], 
                     location_permission: bool = False) -> EmergencyContactList:
        """
        Save emergency contacts for a session.
        
        Args:
            session_id: User session ID
            contacts: List of emergency contacts (1-3)
            location_permission: Whether user granted location permission
            
        Returns:
            EmergencyContactList: Saved contact list
        """
        contact_list = EmergencyContactList(
            session_id=session_id,
            contacts=contacts,
            location_permission=location_permission,
            setup_completed=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._contacts_cache[session_id] = contact_list
        self._save_to_file()
        
        return contact_list
    
    def get_contacts(self, session_id: str) -> Optional[EmergencyContactList]:
        """
        Get emergency contacts for a session.
        
        Args:
            session_id: User session ID
            
        Returns:
            EmergencyContactList or None if not found
        """
        return self._contacts_cache.get(session_id)
    
    def update_contacts(self, session_id: str, contacts: List[EmergencyContact],
                       location_permission: Optional[bool] = None) -> EmergencyContactList:
        """
        Update emergency contacts for a session.
        
        Args:
            session_id: User session ID
            contacts: Updated list of emergency contacts
            location_permission: Updated location permission (optional)
            
        Returns:
            EmergencyContactList: Updated contact list
        """
        existing = self._contacts_cache.get(session_id)
        
        if existing:
            # Update existing
            existing.contacts = contacts
            existing.updated_at = datetime.now()
            if location_permission is not None:
                existing.location_permission = location_permission
            contact_list = existing
        else:
            # Create new
            contact_list = EmergencyContactList(
                session_id=session_id,
                contacts=contacts,
                location_permission=location_permission or False,
                setup_completed=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        self._contacts_cache[session_id] = contact_list
        self._save_to_file()
        
        return contact_list
    
    def delete_contacts(self, session_id: str) -> bool:
        """
        Delete emergency contacts for a session.
        
        Args:
            session_id: User session ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        if session_id in self._contacts_cache:
            del self._contacts_cache[session_id]
            self._save_to_file()
            return True
        return False
    
    def has_contacts(self, session_id: str) -> bool:
        """
        Check if a session has emergency contacts set up.
        
        Args:
            session_id: User session ID
            
        Returns:
            bool: True if contacts exist and setup is complete
        """
        contact_list = self._contacts_cache.get(session_id)
        return contact_list is not None and contact_list.setup_completed
    
    def get_all_sessions(self) -> List[str]:
        """
        Get all session IDs with emergency contacts.
        
        Returns:
            List of session IDs
        """
        return list(self._contacts_cache.keys())
    
    def get_contact_count(self, session_id: str) -> int:
        """
        Get number of contacts for a session.
        
        Args:
            session_id: User session ID
            
        Returns:
            Number of contacts (0 if not found)
        """
        contact_list = self._contacts_cache.get(session_id)
        return len(contact_list.contacts) if contact_list else 0


# Singleton instance
_storage_service = None


def get_storage_service() -> EmergencyStorageService:
    """Get or create singleton storage service instance."""
    global _storage_service
    if _storage_service is None:
        _storage_service = EmergencyStorageService()
    return _storage_service

