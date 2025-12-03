import axios from 'axios';

// API base URL - change this when deploying
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for voice processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service functions
export const apiService = {
  /**
   * Get list of supported languages
   */
  async getLanguages() {
    try {
      const response = await api.get('/api/languages');
      return response.data;
    } catch (error) {
      console.error('Error fetching languages:', error);
      throw error;
    }
  },

  /**
   * Send text message to chatbot
   */
  async sendTextMessage(message, language = 'en', conversationHistory = null) {
    try {
      const response = await api.post('/api/chat', {
        message,
        language,
        conversation_history: conversationHistory,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending text message:', error);
      throw error;
    }
  },

  /**
   * Send voice message to chatbot (complete pipeline)
   */
  async sendVoiceMessage(audioBlob, language = null, sessionId = null) {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');
      
      if (language) {
        formData.append('language', language);
      }
      
      if (sessionId) {
        formData.append('session_id', sessionId);
      }

      const response = await api.post('/api/voice-chat', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error sending voice message:', error);
      throw error;
    }
  },

  /**
   * Transcribe audio only (no LLM response)
   */
  async transcribeAudio(audioBlob, language = 'en') {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');
      formData.append('language', language);

      const response = await api.post('/api/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error transcribing audio:', error);
      throw error;
    }
  },

  /**
   * Get session conversation history
   */
  async getSessionHistory(sessionId) {
    try {
      const response = await api.get(`/api/session/${sessionId}/history`);
      return response.data;
    } catch (error) {
      console.error('Error fetching session history:', error);
      throw error;
    }
  },

  /**
   * Clear session
   */
  async clearSession(sessionId) {
    try {
      const response = await api.delete(`/api/session/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error clearing session:', error);
      throw error;
    }
  },

  /**
   * Health check
   */
  async healthCheck() {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },

  // ===== Coping Strategies API =====

  /**
   * Get personalized coping strategies based on session
   */
  async getPersonalizedStrategies(sessionId = null, language = 'en') {
    try {
      const params = { language };
      if (sessionId) {
        params.session_id = sessionId;
      }
      const response = await api.get('/api/coping/personalized', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching personalized strategies:', error);
      throw error;
    }
  },

  /**
   * Get all coping strategies, optionally filtered by category
   */
  async getAllStrategies(category = null, language = 'en') {
    try {
      const params = { language };
      if (category) {
        params.category = category;
      }
      const response = await api.get('/api/coping/all', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching all strategies:', error);
      throw error;
    }
  },

  /**
   * Get coping strategy categories
   */
  async getCopingCategories(language = 'en') {
    try {
      const response = await api.get('/api/coping/categories', {
        params: { language }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching coping categories:', error);
      throw error;
    }
  },

  /**
   * Get a specific coping strategy by ID
   */
  async getStrategyById(strategyId, language = 'en') {
    try {
      const response = await api.get(`/api/coping/strategy/${strategyId}`, {
        params: { language }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching strategy:', error);
      throw error;
    }
  },

  // ===== Therapist Finder API =====

  /**
   * Search for therapists with filters
   */
  async searchTherapists(filters = {}) {
    try {
      const params = {};
      if (filters.state) params.state = filters.state;
      if (filters.specialty) params.specialty = filters.specialty;
      if (filters.language) params.language = filters.language;
      if (filters.max_price) params.max_price = filters.max_price;
      if (filters.online_only) params.online_only = filters.online_only;

      const response = await api.get('/api/therapists/search', { params });
      return response.data;
    } catch (error) {
      console.error('Error searching therapists:', error);
      throw error;
    }
  },

  /**
   * Get recommended therapists based on conversation
   */
  async getRecommendedTherapists(sessionId = null, location = null) {
    try {
      const params = {};
      if (sessionId) params.session_id = sessionId;
      if (location) params.location = location;

      const response = await api.get('/api/therapists/recommended', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching recommended therapists:', error);
      throw error;
    }
  },

  /**
   * Get all available states with therapist coverage
   */
  async getTherapistStates(language = 'en') {
    try {
      const response = await api.get('/api/therapists/states', {
        params: { lang: language }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching therapist states:', error);
      throw error;
    }
  },

  /**
   * Get all available specialties
   */
  async getTherapistSpecialties(language = 'en') {
    try {
      const response = await api.get('/api/therapists/specialties', {
        params: { lang: language }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching therapist specialties:', error);
      throw error;
    }
  },

  /**
   * Get a specific therapist by ID
   */
  async getTherapistById(therapistId) {
    try {
      const response = await api.get(`/api/therapists/therapist/${therapistId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching therapist:', error);
      throw error;
    }
  },

  /**
   * Get therapists in a specific city
   */
  async getTherapistsByCity(city) {
    try {
      const response = await api.get(`/api/therapists/city/${city}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching therapists by city:', error);
      throw error;
    }
  },
};

export default apiService;

