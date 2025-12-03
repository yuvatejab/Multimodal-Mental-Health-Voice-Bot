from typing import List, Optional, Dict
from groq import Groq
from ..config import settings


class LLMService:
    """LLM service using Groq's Llama model for mental health support."""
    
    def __init__(self):
        """Initialize the LLM service with Groq client."""
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL
        
        # System prompt for mental health support
        self.system_prompt = """You are a compassionate and empathetic mental health support assistant. Your role is to:

1. Listen actively and validate the user's feelings
2. Provide emotional support and encouragement
3. Ask thoughtful questions to help users explore their feelings
4. Suggest healthy coping strategies when appropriate
5. Be non-judgmental and create a safe space for sharing
6. Use a warm, conversational tone

Important guidelines:
- You are NOT a replacement for professional therapy or medical advice
- If someone expresses thoughts of self-harm or suicide, encourage them to seek immediate professional help
- Respect cultural differences and be inclusive
- Keep responses concise but meaningful (2-4 sentences typically)
- Mirror the user's language and communication style
- Be supportive without being patronizing

Remember: Your goal is to provide emotional support and be a caring listener, not to diagnose or treat mental health conditions."""
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        language: str = "en"
    ) -> str:
        """
        Generate a response to the user's message.
        
        Args:
            user_message: The user's input message
            conversation_history: Previous conversation context
            language: Language code for the response
            
        Returns:
            Generated response text
        """
        try:
            # Build messages array
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Keep last 10 messages for context
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Add language instruction if not English
            if language != "en":
                lang_name = settings.SUPPORTED_LANGUAGES.get(language, {}).get("name", language)
                messages.append({
                    "role": "system", 
                    "content": f"Please respond in {lang_name}."
                })
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9,
            )
            
            # Extract response
            response = chat_completion.choices[0].message.content
            return response.strip()
            
        except Exception as e:
            raise Exception(f"Error generating LLM response: {str(e)}")
    
    async def detect_crisis(self, text: str) -> bool:
        """
        Detect if the message contains crisis indicators.
        
        Args:
            text: User's message text
            
        Returns:
            True if crisis indicators are detected
        """
        # Crisis keywords and phrases
        crisis_keywords = [
            "suicide", "kill myself", "end my life", "want to die",
            "self harm", "hurt myself", "cutting", "overdose",
            "no reason to live", "better off dead", "can't go on",
            "ending it all", "goodbye forever"
        ]
        
        text_lower = text.lower()
        
        # Check for crisis keywords
        for keyword in crisis_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    async def get_crisis_response(self, language: str = "en") -> str:
        """
        Get an appropriate crisis response.
        
        Args:
            language: Language code for the response
            
        Returns:
            Crisis support message
        """
        crisis_responses = {
            "en": """I'm really concerned about what you're sharing. Please know that you don't have to face this alone. 

I strongly encourage you to reach out to a crisis helpline right away:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

These services are available 24/7 with trained professionals who can provide immediate support. Your life matters, and there are people who want to help.""",
            
            "hi": """मुझे आपकी बातों से बहुत चिंता हो रही है। कृपया जानें कि आपको इसका सामना अकेले नहीं करना है।

मैं आपसे आग्रह करता हूं कि तुरंत किसी संकट हेल्पलाइन से संपर्क करें:
- AASRA: 91-9820466726
- Vandrevala Foundation: 1860-2662-345
- iCall: 91-22-25521111

ये सेवाएं 24/7 उपलब्ध हैं। आपका जीवन महत्वपूर्ण है, और लोग आपकी मदद करना चाहते हैं।""",
            
            "es": """Me preocupa mucho lo que estás compartiendo. Por favor, sabe que no tienes que enfrentar esto solo.

Te animo a que contactes una línea de crisis de inmediato:
- Línea Nacional de Prevención del Suicidio: 988 (EE.UU.)
- Crisis Text Line: Envía HOLA al 741741

Estos servicios están disponibles 24/7. Tu vida importa y hay personas que quieren ayudarte.""",
        }
        
        return crisis_responses.get(language, crisis_responses["en"])

