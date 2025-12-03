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
        self.system_prompt = """You are a compassionate and empathetic mental health support assistant for users primarily in India. Your role is to:

1. Listen actively and validate the user's feelings
2. Provide emotional support and encouragement
3. Ask thoughtful questions to help users explore their feelings
4. Suggest healthy coping strategies when appropriate
5. Be non-judgmental and create a safe space for sharing
6. Use a warm, conversational tone
7. Be culturally sensitive to Indian context, family dynamics, and social norms

Important guidelines:
- You are NOT a replacement for professional therapy or medical advice
- If someone expresses thoughts of self-harm or suicide, encourage them to seek immediate professional help from Indian crisis helplines
- Respect cultural differences, family values, and be inclusive
- Keep responses concise but meaningful (2-4 sentences typically)
- Mirror the user's language and communication style
- Be supportive without being patronizing
- Understand the stigma around mental health in India and be extra supportive

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
        Detect if the message contains crisis indicators using both keywords and LLM.
        
        Args:
            text: User's message text
            
        Returns:
            True if crisis indicators are detected
        """
        # Multilingual crisis keywords and phrases
        crisis_keywords = [
            # English
            "suicide", "suicidal", "kill myself", "end my life", "want to die",
            "self harm", "hurt myself", "cutting", "overdose", "jump", "jumping",
            "no reason to live", "better off dead", "can't go on", "ending it all", 
            "goodbye forever", "hang myself", "hanging", "want to hurt",
            
            # Hindi (Devanagari)
            "आत्महत्या", "खुदकुशी", "मरना चाहता", "मरना चाहती", "जान देना", 
            "मौत", "कूदना", "कूदूंगा", "कूदूंगी", "खुद को मार", "आत्महत्या करना",
            "जीना नहीं चाहता", "जीना नहीं चाहती", "जीवन समाप्त", "छोड़ देना चाहता",
            
            # Hindi (Romanized/Hinglish)
            "mar jaana", "kud jaana", "khudkushi", "aatmahatya", "jeena nahi chahta",
            "marna chahta", "jump kar", "building se kud"
        ]
        
        text_lower = text.lower()
        
        # First check: keyword matching
        for keyword in crisis_keywords:
            if keyword in text_lower:
                print(f"Crisis keyword detected: {keyword}")
                return True
        
        # Second check: Use LLM for intelligent crisis detection
        # This catches cases that keywords might miss
        try:
            crisis_check_prompt = f"""Analyze this message for crisis indicators (suicide, self-harm, immediate danger).
Respond with ONLY "YES" or "NO".

Message: "{text}"

Is this a crisis situation requiring immediate mental health intervention?"""

            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a crisis detection system. Respond only with YES or NO."},
                    {"role": "user", "content": crisis_check_prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=10,
            )
            
            llm_result = response.choices[0].message.content.strip().upper()
            
            if "YES" in llm_result:
                print(f"Crisis detected by LLM analysis")
                return True
                
        except Exception as e:
            print(f"LLM crisis detection failed: {e}, falling back to keyword-only")
        
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
            "en": """I hear you, and I'm deeply concerned. You don't have to face this alone—help is available right now.

🆘 Immediate Crisis Support (India):
• AASRA: 91-9820466726 (24/7)
• Vandrevala Foundation: 1860-266-2345 (24/7, Free)
• Kiran Helpline: 1800-599-0019 (24/7, Toll-free)
• iCall: 022-25521111 (Mon-Sat, 8 AM-10 PM)

🏥 Walk-in Support:
• NIMHANS Bangalore: 080-46110007
• Fortis Stress Helpline: 8376804102
• Visit your nearest government hospital emergency

Your life has value. These professionals understand what you're going through and want to help.""",
            
            "hi": """मैं आपकी बात सुन रहा हूं और मुझे आपकी बहुत चिंता है। आपको अकेले नहीं रहना है—मदद अभी उपलब्ध है।

🆘 तुरंत संकट सहायता (भारत):
• आसरा (AASRA): 91-9820466726 (24/7)
• वंद्रेवाला फाउंडेशन: 1860-266-2345 (24/7, निःशुल्क)
• किरण हेल्पलाइन: 1800-599-0019 (24/7, टोल-फ्री)
• आईकॉल (iCall): 022-25521111 (सोम-शनि, 8 AM-10 PM)

🏥 अस्पताल सहायता:
• निमहंस बैंगलोर: 080-46110007
• फोर्टिस स्ट्रेस हेल्पलाइन: 8376804102
• नजदीकी सरकारी अस्पताल की इमरजेंसी में जाएं

आपका जीवन मूल्यवान है। ये पेशेवर आपकी स्थिति समझते हैं और मदद करना चाहते हैं।""",
            
            "es": """Me preocupa mucho lo que estás compartiendo. Por favor, sabe que no tienes que enfrentar esto solo.

Te animo a que contactes una línea de crisis de inmediato:
- Línea Nacional de Prevención del Suicidio: 988 (EE.UU.)
- Crisis Text Line: Envía HOLA al 741741

Estos servicios están disponibles 24/7. Tu vida importa y hay personas que quieren ayudarte.""",
        }
        
        return crisis_responses.get(language, crisis_responses["en"])

