from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from ..services.coping_service import CopingService
from ..services.therapy_service import TherapyService

router = APIRouter()

# Initialize services
coping_service = CopingService()
therapy_service = TherapyService()


@router.get("/personalized")
async def get_personalized_strategies(
    session_id: Optional[str] = Query(None, description="Session ID for conversation context"),
    language: str = Query("en", description="Language code (en, hi, etc.)"),
):
    """
    Get personalized coping strategies based on user's conversation history.
    
    Args:
        session_id: Optional session ID to analyze conversation
        language: Language code
        
    Returns:
        List of personalized coping strategies
    """
    try:
        # Get conversation context and detected emotions from session
        detected_emotions = None
        conversation_context = None
        
        if session_id:
            # Get session data from therapy service
            session = therapy_service.get_session(session_id)
            
            if session:
                # Extract emotions from conversation history
                conversation_history = session.get("conversation_history", [])
                
                # Create a summary of the conversation for context
                if conversation_history:
                    recent_messages = conversation_history[-6:]  # Last 3 exchanges
                    conversation_context = " ".join([
                        msg.get("content", "") 
                        for msg in recent_messages 
                        if msg.get("role") == "user"
                    ])
                
                # Try to infer emotions from conversation
                # For now, we'll use common emotions; could be enhanced with emotion service
                detected_emotions = ["stress", "anxiety"]  # Default
                
                # Check if crisis was detected
                if session.get("crisis_detected"):
                    detected_emotions = ["panic", "crisis", "anxiety"]
        
        # Get personalized strategies
        strategies = await coping_service.get_personalized_strategies(
            session_id=session_id,
            language=language,
            conversation_context=conversation_context,
            detected_emotions=detected_emotions
        )
        
        return {
            "success": True,
            "strategies": strategies,
            "count": len(strategies)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting personalized strategies: {str(e)}")


@router.get("/all")
async def get_all_strategies(
    category: Optional[str] = Query(None, description="Filter by category (breathing, grounding, mindfulness, cbt, physical)"),
    language: str = Query("en", description="Language code (en, hi, etc.)"),
):
    """
    Get all coping strategies, optionally filtered by category.
    
    Args:
        category: Optional category filter
        language: Language code
        
    Returns:
        List of coping strategies
    """
    try:
        strategies = coping_service.get_all_strategies(
            category=category,
            language=language
        )
        
        return {
            "success": True,
            "strategies": strategies,
            "count": len(strategies),
            "category": category
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting strategies: {str(e)}")


@router.get("/categories")
async def get_categories(
    language: str = Query("en", description="Language code (en, hi, etc.)"),
):
    """
    Get all available coping strategy categories.
    
    Args:
        language: Language code
        
    Returns:
        List of categories
    """
    try:
        categories = coping_service.get_categories(language=language)
        
        return {
            "success": True,
            "categories": categories,
            "count": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories: {str(e)}")


@router.get("/strategy/{strategy_id}")
async def get_strategy_by_id(
    strategy_id: str,
    language: str = Query("en", description="Language code (en, hi, etc.)"),
):
    """
    Get a specific coping strategy by ID.
    
    Args:
        strategy_id: Strategy ID
        language: Language code
        
    Returns:
        Strategy details
    """
    try:
        strategy = coping_service.get_strategy_by_id(
            strategy_id=strategy_id,
            language=language
        )
        
        if not strategy:
            raise HTTPException(status_code=404, detail=f"Strategy with ID '{strategy_id}' not found")
        
        return {
            "success": True,
            "strategy": strategy
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting strategy: {str(e)}")

