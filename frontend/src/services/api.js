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
};

export default apiService;

