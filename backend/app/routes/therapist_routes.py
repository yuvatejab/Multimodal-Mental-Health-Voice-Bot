from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from ..services.therapist_service import TherapistService
from ..services.therapy_service import TherapyService

router = APIRouter()

# Initialize services
therapist_service = TherapistService()
therapy_service = TherapyService()


@router.get("/search")
async def search_therapists(
    state: Optional[str] = Query(None, description="State name to filter by"),
    specialty: Optional[str] = Query(None, description="Specialty to filter by"),
    language: Optional[str] = Query(None, description="Language spoken by therapist"),
    max_price: Optional[int] = Query(None, description="Maximum consultation fee"),
    online_only: bool = Query(False, description="Only show online therapists"),
):
    """
    Search for therapists based on various filters.
    
    Args:
        state: State name
        specialty: Specialty ID
        language: Language name
        max_price: Maximum price
        online_only: Online availability filter
        
    Returns:
        List of matching therapists
    """
    try:
        therapists = therapist_service.search_therapists(
            state=state,
            specialty=specialty,
            language=language,
            max_price=max_price,
            online_only=online_only
        )
        
        return {
            "success": True,
            "therapists": therapists,
            "count": len(therapists),
            "filters": {
                "state": state,
                "specialty": specialty,
                "language": language,
                "max_price": max_price,
                "online_only": online_only
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching therapists: {str(e)}")


@router.get("/recommended")
async def get_recommended_therapists(
    session_id: Optional[str] = Query(None, description="Session ID for conversation context"),
    location: Optional[str] = Query(None, description="User's location (state or city)"),
):
    """
    Get recommended therapists based on user's conversation and needs.
    
    Args:
        session_id: Optional session ID to analyze conversation
        location: Optional user location
        
    Returns:
        List of recommended therapists
    """
    try:
        # Get conversation context from session
        conversation_context = None
        
        if session_id:
            session = therapy_service.get_session(session_id)
            
            if session:
                # Extract recent conversation
                conversation_history = session.get("conversation_history", [])
                
                if conversation_history:
                    recent_messages = conversation_history[-6:]  # Last 3 exchanges
                    conversation_context = " ".join([
                        msg.get("content", "") 
                        for msg in recent_messages 
                        if msg.get("role") == "user"
                    ])
        
        # Get recommended therapists
        therapists = await therapist_service.get_recommended_therapists(
            session_id=session_id,
            location=location,
            conversation_context=conversation_context
        )
        
        return {
            "success": True,
            "therapists": therapists,
            "count": len(therapists),
            "personalized": bool(conversation_context)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommended therapists: {str(e)}")


@router.get("/states")
async def get_states(
    lang: str = Query("en", description="Language code (en, hi, etc.)"),
):
    """
    Get all available states with therapist coverage.
    
    Args:
        lang: Language code
        
    Returns:
        List of states
    """
    try:
        states = therapist_service.get_all_states(language=lang)
        
        return {
            "success": True,
            "states": states,
            "count": len(states)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting states: {str(e)}")


@router.get("/specialties")
async def get_specialties(
    lang: str = Query("en", description="Language code (en, hi, etc.)"),
):
    """
    Get all available specialties.
    
    Args:
        lang: Language code
        
    Returns:
        List of specialties
    """
    try:
        specialties = therapist_service.get_all_specialties(language=lang)
        
        return {
            "success": True,
            "specialties": specialties,
            "count": len(specialties)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting specialties: {str(e)}")


@router.get("/therapist/{therapist_id}")
async def get_therapist_by_id(
    therapist_id: str,
):
    """
    Get a specific therapist by ID.
    
    Args:
        therapist_id: Therapist ID
        
    Returns:
        Therapist details
    """
    try:
        therapist = therapist_service.get_therapist_by_id(therapist_id)
        
        if not therapist:
            raise HTTPException(status_code=404, detail=f"Therapist with ID '{therapist_id}' not found")
        
        return {
            "success": True,
            "therapist": therapist
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting therapist: {str(e)}")


@router.get("/city/{city}")
async def get_therapists_by_city(
    city: str,
):
    """
    Get all therapists in a specific city.
    
    Args:
        city: City name
        
    Returns:
        List of therapists in that city
    """
    try:
        therapists = therapist_service.get_therapists_by_city(city)
        
        return {
            "success": True,
            "therapists": therapists,
            "count": len(therapists),
            "city": city
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting therapists by city: {str(e)}")

