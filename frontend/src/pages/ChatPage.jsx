import React, { useState, useEffect } from 'react';
import { Heart, Sparkles, RefreshCw } from 'lucide-react';
import VoiceRecorder from '../components/VoiceRecorder';
import ChatInterface from '../components/ChatInterface';
import LanguageSelector from '../components/LanguageSelector';
import ActionButtons from '../components/ActionButtons';
import apiService from '../services/api';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState(
    localStorage.getItem('preferredLanguage') || 'en'
  );
  const [selectedLanguageName, setSelectedLanguageName] = useState(
    localStorage.getItem('preferredLanguageName') || 'English'
  );
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentPlayingId, setCurrentPlayingId] = useState(null);
  const [showCrisisHelp, setShowCrisisHelp] = useState(false);

  useEffect(() => {
    // Generate session ID
    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
    localStorage.setItem('currentSessionId', newSessionId);
    
    // Check backend health
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await apiService.healthCheck();
    } catch (err) {
      console.error('Backend health check failed:', err);
      setError('Unable to connect to the server. Please make sure the backend is running.');
    }
  };

  const handleLanguageChange = (code, name) => {
    setSelectedLanguage(code);
    setSelectedLanguageName(name);
  };

  const handleRecordingComplete = async (audioBlob) => {
    setIsProcessing(true);
    setError(null);

    try {
      // Send voice message to backend
      const response = await apiService.sendVoiceMessage(
        audioBlob,
        selectedLanguage,
        sessionId
      );

      // Add user message (transcription)
      const userMessage = {
        id: `msg_${Date.now()}_user`,
        role: 'user',
        text: response.transcription,
        transcription: response.transcription,
        timestamp: new Date().toISOString(),
      };

      // Add bot response
      const botMessage = {
        id: `msg_${Date.now()}_bot`,
        role: 'assistant',
        text: response.response,
        audioBase64: response.audio_base64,
        isCrisis: response.is_crisis,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage, botMessage]);

      // Show crisis help if detected
      if (response.is_crisis) {
        setShowCrisisHelp(true);
      }

      // Auto-play the audio response
      if (response.audio_base64) {
        playAudioResponse(response.audio_base64, botMessage.id);
      }

    } catch (err) {
      console.error('Error processing voice message:', err);
      setError('Failed to process your message. Please try again.');
      
      // Add error message to chat
      const errorMessage = {
        id: `msg_${Date.now()}_error`,
        role: 'assistant',
        text: 'I apologize, but I encountered an error processing your message. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const playAudioResponse = (audioBase64, messageId) => {
    try {
      setIsPlaying(true);
      setCurrentPlayingId(messageId);

      const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
      
      audio.onended = () => {
        setIsPlaying(false);
        setCurrentPlayingId(null);
      };

      audio.onerror = () => {
        setIsPlaying(false);
        setCurrentPlayingId(null);
        console.error('Error playing audio');
      };

      audio.play();
    } catch (err) {
      console.error('Error playing audio:', err);
      setIsPlaying(false);
      setCurrentPlayingId(null);
    }
  };

  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear the conversation?')) {
      setMessages([]);
      const newSessionId = `session_${Date.now()}`;
      setSessionId(newSessionId);
      localStorage.setItem('currentSessionId', newSessionId);
      setError(null);
      setShowCrisisHelp(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="glass-effect border-b border-white/20 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-r from-primary-500 to-secondary-500 p-2 rounded-xl">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                Mental Health Voice Bot
              </h1>
              <p className="text-xs text-gray-500">Your compassionate AI companion</p>
            </div>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <ActionButtons showInHeader={true} />
            
            <LanguageSelector
              selectedLanguage={selectedLanguage}
              onLanguageChange={handleLanguageChange}
            />
            
            {messages.length > 0 && (
              <button
                onClick={handleClearChat}
                className="glass-effect rounded-full p-2 hover:shadow-lg transition-all duration-300"
                aria-label="Clear conversation"
                title="Clear conversation"
              >
                <RefreshCw className="w-4 h-4 text-gray-600" />
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-b border-red-200 px-4 py-3">
          <div className="max-w-6xl mx-auto flex items-center gap-2 text-red-800 text-sm">
            <span className="font-medium">Error:</span>
            <span>{error}</span>
            <button 
              onClick={() => setError(null)}
              className="ml-auto text-red-600 hover:text-red-800"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 flex flex-col max-w-6xl w-full mx-auto">
        {/* Crisis Help Section */}
        {showCrisisHelp && (
          <div className="p-4">
            <ActionButtons isCrisis={true} />
          </div>
        )}

        {/* Action Buttons (shown when no messages) */}
        {messages.length === 0 && (
          <div className="p-4">
            <ActionButtons />
          </div>
        )}

        {/* Chat Messages */}
        <ChatInterface 
          messages={messages}
          isPlaying={isPlaying}
          currentPlayingId={currentPlayingId}
        />

        {/* Voice Recorder Section */}
        <div className="glass-effect border-t border-white/20 p-6">
          <div className="max-w-2xl mx-auto">
            <VoiceRecorder
              onRecordingComplete={handleRecordingComplete}
              isProcessing={isProcessing}
              language={selectedLanguageName}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="glass-effect border-t border-white/20 py-4">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
            <Sparkles className="w-4 h-4 text-secondary-500" />
            <span>
              This is a support tool, not a replacement for professional mental health care
            </span>
          </div>
          <div className="mt-2 text-xs text-gray-400">
            If you're in crisis, please contact emergency services or a crisis helpline immediately
          </div>
        </div>
      </footer>
    </div>
  );
}

export default ChatPage;

