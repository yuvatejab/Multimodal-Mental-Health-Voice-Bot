import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from ..services.llm_service import LLMService
from ..services.therapy_service import TherapyService


class CopingService:
    """Service for providing personalized coping strategies and exercises."""
    
    def __init__(self):
        """Initialize the coping service."""
        self.llm_service = LLMService()
        self.strategies_data = self._load_strategies()
    
    def _load_strategies(self) -> Dict:
        """Load coping strategies from JSON file."""
        try:
            # Get the path to the data file
            current_dir = Path(__file__).parent.parent
            data_file = current_dir / "data" / "coping_strategies.json"
            
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading coping strategies: {e}")
            return {"strategies": [], "categories": []}
    
    async def get_personalized_strategies(
        self,
        session_id: Optional[str] = None,
        language: str = "en",
        conversation_context: Optional[str] = None,
        detected_emotions: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Get personalized coping strategies based on user's conversation and emotions.
        
        Args:
            session_id: Session ID to analyze conversation history
            language: Language code (en, hi, etc.)
            conversation_context: Optional conversation summary
            detected_emotions: List of detected emotions
            
        Returns:
            List of personalized coping strategies
        """
        try:
            # If no emotions provided, use general strategies
            if not detected_emotions:
                detected_emotions = ["stress", "anxiety"]
            
            # Filter strategies by detected emotions
            relevant_strategies = []
            for strategy in self.strategies_data.get("strategies", []):
                # Check if strategy matches any detected emotion
                when_to_use = strategy.get("when_to_use", [])
                if any(emotion in when_to_use for emotion in detected_emotions):
                    relevant_strategies.append(strategy)
            
            # If we have too few strategies, add some general ones
            if len(relevant_strategies) < 5:
                for strategy in self.strategies_data.get("strategies", []):
                    if strategy not in relevant_strategies:
                        relevant_strategies.append(strategy)
                    if len(relevant_strategies) >= 8:
                        break
            
            # Limit to top 8 strategies
            relevant_strategies = relevant_strategies[:8]
            
            # Personalize descriptions using LLM if conversation context is provided
            if conversation_context:
                relevant_strategies = await self._personalize_descriptions(
                    relevant_strategies,
                    conversation_context,
                    language
                )
            
            # Format strategies for the specified language
            formatted_strategies = self._format_for_language(relevant_strategies, language)
            
            return formatted_strategies
            
        except Exception as e:
            print(f"Error getting personalized strategies: {e}")
            # Return some default strategies
            return self._format_for_language(
                self.strategies_data.get("strategies", [])[:5],
                language
            )
    
    async def _personalize_descriptions(
        self,
        strategies: List[Dict],
        conversation_context: str,
        language: str
    ) -> List[Dict]:
        """
        Use LLM to personalize strategy descriptions based on conversation context.
        
        Args:
            strategies: List of strategies
            conversation_context: Summary of user's conversation
            language: Language code
            
        Returns:
            Strategies with personalized descriptions
        """
        try:
            # Create a prompt for the LLM
            strategy_names = [s.get("name", "") for s in strategies]
            
            prompt = f"""Based on this user's situation: "{conversation_context}"
            
Suggest which of these coping strategies would be most helpful (rank top 5):
{', '.join(strategy_names)}

Respond with just the strategy names in order of relevance, separated by commas."""
            
            response = await self.llm_service.generate_response(
                user_message=prompt,
                conversation_history=[],
                language=language
            )
            
            # Parse the response to reorder strategies
            suggested_order = [s.strip() for s in response.split(',')]
            
            # Reorder strategies based on LLM suggestion
            reordered = []
            for suggested_name in suggested_order:
                for strategy in strategies:
                    if suggested_name.lower() in strategy.get("name", "").lower():
                        if strategy not in reordered:
                            reordered.append(strategy)
            
            # Add any remaining strategies
            for strategy in strategies:
                if strategy not in reordered:
                    reordered.append(strategy)
            
            return reordered
            
        except Exception as e:
            print(f"Error personalizing descriptions: {e}")
            return strategies
    
    def _format_for_language(self, strategies: List[Dict], language: str) -> List[Dict]:
        """
        Format strategies for the specified language.
        
        Args:
            strategies: List of strategies
            language: Language code
            
        Returns:
            Formatted strategies
        """
        formatted = []
        
        for strategy in strategies:
            formatted_strategy = {
                "id": strategy.get("id"),
                "name": strategy.get(f"name_{language}", strategy.get("name")),
                "category": strategy.get("category"),
                "difficulty": strategy.get("difficulty"),
                "duration_minutes": strategy.get("duration_minutes"),
                "description": strategy.get(f"description_{language}", strategy.get("description")),
                "when_to_use": strategy.get("when_to_use", []),
                "steps": strategy.get(f"steps_{language}", strategy.get("steps", [])),
                "video_url": strategy.get("video_url"),
                "scientific_basis": strategy.get("scientific_basis"),
                "external_links": strategy.get("external_links", [])
            }
            formatted.append(formatted_strategy)
        
        return formatted
    
    def get_all_strategies(
        self,
        category: Optional[str] = None,
        language: str = "en"
    ) -> List[Dict]:
        """
        Get all coping strategies, optionally filtered by category.
        
        Args:
            category: Optional category filter (breathing, grounding, mindfulness, cbt, physical)
            language: Language code
            
        Returns:
            List of coping strategies
        """
        strategies = self.strategies_data.get("strategies", [])
        
        # Filter by category if specified
        if category:
            strategies = [s for s in strategies if s.get("category") == category]
        
        # Format for language
        return self._format_for_language(strategies, language)
    
    def get_categories(self, language: str = "en") -> List[Dict]:
        """
        Get all available strategy categories.
        
        Args:
            language: Language code
            
        Returns:
            List of categories with names and descriptions
        """
        categories = self.strategies_data.get("categories", [])
        
        formatted = []
        for category in categories:
            formatted_category = {
                "id": category.get("id"),
                "name": category.get(f"name_{language}", category.get("name")),
                "description": category.get(f"description_{language}", category.get("description"))
            }
            formatted.append(formatted_category)
        
        return formatted
    
    def get_strategy_by_id(self, strategy_id: str, language: str = "en") -> Optional[Dict]:
        """
        Get a specific strategy by ID.
        
        Args:
            strategy_id: Strategy ID
            language: Language code
            
        Returns:
            Strategy dict or None if not found
        """
        for strategy in self.strategies_data.get("strategies", []):
            if strategy.get("id") == strategy_id:
                return self._format_for_language([strategy], language)[0]
        
        return None

