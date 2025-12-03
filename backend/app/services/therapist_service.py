import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from ..services.llm_service import LLMService


class TherapistService:
    """Service for finding and recommending therapists."""
    
    def __init__(self):
        """Initialize the therapist service."""
        self.llm_service = LLMService()
        self.therapists_data = self._load_therapists()
    
    def _load_therapists(self) -> Dict:
        """Load therapists from JSON file."""
        try:
            # Get the path to the data file
            current_dir = Path(__file__).parent.parent
            data_file = current_dir / "data" / "therapists.json"
            
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading therapists: {e}")
            return {"therapists": [], "specialties": [], "states": []}
    
    def search_therapists(
        self,
        state: Optional[str] = None,
        specialty: Optional[str] = None,
        language: Optional[str] = None,
        max_price: Optional[int] = None,
        online_only: bool = False
    ) -> List[Dict]:
        """
        Search for therapists based on filters.
        
        Args:
            state: State name to filter by
            specialty: Specialty to filter by
            language: Language to filter by
            max_price: Maximum consultation fee
            online_only: Only show therapists offering online consultations
            
        Returns:
            List of matching therapists
        """
        therapists = self.therapists_data.get("therapists", [])
        
        # Apply filters
        filtered = []
        for therapist in therapists:
            # State filter
            if state and therapist.get("state") != state:
                continue
            
            # Specialty filter
            if specialty and specialty not in therapist.get("specialties", []):
                continue
            
            # Language filter
            if language:
                therapist_languages = [lang.lower() for lang in therapist.get("languages", [])]
                if language.lower() not in therapist_languages:
                    continue
            
            # Price filter
            if max_price and therapist.get("consultation_fee_min", 0) > max_price:
                continue
            
            # Online availability filter
            if online_only and not therapist.get("online_available", False):
                continue
            
            filtered.append(therapist)
        
        # Sort by rating (highest first)
        filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        return filtered
    
    async def get_recommended_therapists(
        self,
        session_id: Optional[str] = None,
        location: Optional[str] = None,
        conversation_context: Optional[str] = None
    ) -> List[Dict]:
        """
        Get recommended therapists based on user's conversation and needs.
        
        Args:
            session_id: Session ID to analyze conversation
            location: User's location (state or city)
            conversation_context: Summary of user's concerns
            
        Returns:
            List of recommended therapists
        """
        try:
            # Identify needed specialties from conversation
            needed_specialties = []
            
            if conversation_context:
                # Use LLM to identify specialties
                prompt = f"""Based on this user's concerns: "{conversation_context}"
                
Which of these mental health specialties would be most helpful?
{', '.join([s['id'] for s in self.therapists_data.get('specialties', [])])}

Respond with just the specialty IDs that match, separated by commas (maximum 3)."""
                
                try:
                    response = await self.llm_service.generate_response(
                        user_message=prompt,
                        conversation_history=[],
                        language="en"
                    )
                    
                    # Parse the response
                    suggested_specialties = [s.strip() for s in response.split(',')]
                    needed_specialties = suggested_specialties[:3]
                    
                except Exception as e:
                    print(f"Error getting specialty recommendations: {e}")
                    # Default to common specialties
                    needed_specialties = ["anxiety", "depression", "stress_management"]
            else:
                # Default specialties
                needed_specialties = ["anxiety", "depression", "stress_management"]
            
            # Search for therapists with these specialties
            recommended = []
            
            for specialty in needed_specialties:
                matching = self.search_therapists(
                    state=location if location else None,
                    specialty=specialty
                )
                
                for therapist in matching:
                    # Avoid duplicates
                    if not any(t.get("id") == therapist.get("id") for t in recommended):
                        recommended.append(therapist)
                
                # Limit to top 10
                if len(recommended) >= 10:
                    break
            
            # If no location-specific therapists found, get top-rated ones
            if not recommended:
                all_therapists = self.therapists_data.get("therapists", [])
                all_therapists.sort(key=lambda x: x.get("rating", 0), reverse=True)
                recommended = all_therapists[:10]
            
            return recommended[:10]  # Return top 10
            
        except Exception as e:
            print(f"Error getting recommended therapists: {e}")
            # Return top-rated therapists as fallback
            all_therapists = self.therapists_data.get("therapists", [])
            all_therapists.sort(key=lambda x: x.get("rating", 0), reverse=True)
            return all_therapists[:10]
    
    def get_all_states(self, language: str = "en") -> List[Dict]:
        """
        Get all available states with therapist coverage.
        
        Args:
            language: Language code
            
        Returns:
            List of states
        """
        states = self.therapists_data.get("states", [])
        
        # Format for language
        formatted = []
        for state in states:
            formatted_state = {
                "id": state.get("id"),
                "name": state.get(f"name_{language}", state.get("name")),
                "therapist_count": state.get("therapist_count", 0)
            }
            formatted.append(formatted_state)
        
        return formatted
    
    def get_all_specialties(self, language: str = "en") -> List[Dict]:
        """
        Get all available specialties.
        
        Args:
            language: Language code
            
        Returns:
            List of specialties
        """
        specialties = self.therapists_data.get("specialties", [])
        
        # Format for language
        formatted = []
        for specialty in specialties:
            formatted_specialty = {
                "id": specialty.get("id"),
                "name": specialty.get(f"name_{language}", specialty.get("name"))
            }
            formatted.append(formatted_specialty)
        
        return formatted
    
    def get_therapist_by_id(self, therapist_id: str) -> Optional[Dict]:
        """
        Get a specific therapist by ID.
        
        Args:
            therapist_id: Therapist ID
            
        Returns:
            Therapist dict or None if not found
        """
        for therapist in self.therapists_data.get("therapists", []):
            if therapist.get("id") == therapist_id:
                return therapist
        
        return None
    
    def get_therapists_by_city(self, city: str) -> List[Dict]:
        """
        Get therapists in a specific city.
        
        Args:
            city: City name
            
        Returns:
            List of therapists in that city
        """
        therapists = self.therapists_data.get("therapists", [])
        
        city_therapists = [
            t for t in therapists 
            if t.get("city", "").lower() == city.lower()
        ]
        
        # Sort by rating
        city_therapists.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        return city_therapists

