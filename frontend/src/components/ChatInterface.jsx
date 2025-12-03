import React, { useEffect, useRef, useState } from 'react';
import { Volume2, User, Bot, AlertCircle } from 'lucide-react';

const ChatInterface = ({ messages, isPlaying, currentPlayingId }) => {
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const playAudio = (audioBase64, messageId) => {
    if (audioRef.current) {
      audioRef.current.pause();
    }

    const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
    audioRef.current = audio;
    
    audio.play().catch(err => {
      console.error('Error playing audio:', err);
    });
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-center px-4">
          <div className="glass-effect rounded-3xl p-8 max-w-md">
            <Bot className="w-16 h-16 mx-auto mb-4 text-primary-500" />
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Welcome to Your Safe Space
            </h2>
            <p className="text-gray-600 mb-4">
              I'm here to listen and support you. Share what's on your mind, 
              and I'll respond with empathy and care.
            </p>
            <div className="text-sm text-gray-500 space-y-2">
              <p>✓ Voice-first experience</p>
              <p>✓ Multilingual support</p>
              <p>✓ Confidential and judgment-free</p>
            </div>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
            >
              <div className={`flex gap-3 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar */}
                <div className={`
                  flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center
                  ${message.role === 'user' 
                    ? 'bg-gradient-to-r from-primary-500 to-primary-600' 
                    : 'bg-gradient-to-r from-secondary-500 to-secondary-600'
                  }
                `}>
                  {message.role === 'user' ? (
                    <User className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-white" />
                  )}
                </div>

                {/* Message Content */}
                <div className="flex flex-col gap-1">
                  <div className={`
                    message-bubble
                    ${message.role === 'user' ? 'message-user' : 'message-bot'}
                  `}>
                    {/* Crisis Warning */}
                    {message.isCrisis && (
                      <div className="flex items-start gap-2 mb-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                        <div className="text-sm text-red-800">
                          <strong>Important:</strong> This message contains crisis indicators. 
                          Please consider reaching out to professional help.
                        </div>
                      </div>
                    )}

                    {/* Transcription (for user messages from voice) */}
                    {message.transcription && message.role === 'user' && (
                      <div className="text-sm opacity-75 mb-2 italic">
                        "{message.transcription}"
                      </div>
                    )}

                    {/* Main message text */}
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {message.text}
                    </div>

                    {/* Audio playback button for bot messages */}
                    {message.audioBase64 && message.role === 'assistant' && (
                      <button
                        onClick={() => playAudio(message.audioBase64, message.id)}
                        className="mt-3 flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 transition-colors"
                        aria-label="Play audio response"
                      >
                        <Volume2 className={`w-4 h-4 ${isPlaying && currentPlayingId === message.id ? 'animate-pulse' : ''}`} />
                        <span>Play audio</span>
                      </button>
                    )}
                  </div>

                  {/* Timestamp */}
                  <div className={`text-xs text-gray-400 px-2 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                    {formatTimestamp(message.timestamp)}
                  </div>
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
};

export default ChatInterface;

