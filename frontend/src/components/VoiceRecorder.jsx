import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Loader2 } from 'lucide-react';

const VoiceRecorder = ({ onRecordingComplete, isProcessing, language }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [error, setError] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (mediaRecorderRef.current && isRecording) {
        mediaRecorderRef.current.stop();
      }
    };
  }, [isRecording]);

  const startRecording = async () => {
    try {
      setError(null);
      
      // Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
        } 
      });

      // Create MediaRecorder
      const mimeType = MediaRecorder.isTypeSupported('audio/webm') 
        ? 'audio/webm' 
        : 'audio/mp4';
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      // Handle data available
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      // Handle recording stop
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        
        // Send to parent component
        if (onRecordingComplete) {
          onRecordingComplete(audioBlob);
        }
        
        // Reset
        audioChunksRef.current = [];
        setRecordingTime(0);
      };

      // Start recording
      mediaRecorder.start();
      setIsRecording(true);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (err) {
      console.error('Error starting recording:', err);
      setError('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex flex-col items-center gap-4">
      {error && (
        <div className="text-red-500 text-sm bg-red-50 px-4 py-2 rounded-lg">
          {error}
        </div>
      )}

      <div className="flex items-center gap-4">
        {/* Recording Button */}
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
          className={`
            relative w-20 h-20 rounded-full flex items-center justify-center
            transition-all duration-300 shadow-lg
            ${isRecording 
              ? 'bg-red-500 hover:bg-red-600 recording-indicator' 
              : 'bg-gradient-to-r from-primary-500 to-secondary-500 hover:scale-110'
            }
            ${isProcessing ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-xl'}
          `}
          aria-label={isRecording ? 'Stop recording' : 'Start recording'}
        >
          {isProcessing ? (
            <Loader2 className="w-8 h-8 text-white animate-spin" />
          ) : isRecording ? (
            <MicOff className="w-8 h-8 text-white" />
          ) : (
            <Mic className="w-8 h-8 text-white" />
          )}
          
          {/* Pulse effect when recording */}
          {isRecording && (
            <>
              <span className="absolute inset-0 rounded-full bg-red-500 opacity-75 animate-ping" />
              <span className="absolute inset-0 rounded-full bg-red-500 opacity-50 animate-pulse" />
            </>
          )}
        </button>
      </div>

      {/* Recording Status */}
      <div className="text-center">
        {isRecording && (
          <div className="flex flex-col items-center gap-2 animate-fade-in">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
              <span className="text-lg font-medium text-gray-700">
                Recording...
              </span>
            </div>
            <span className="text-2xl font-mono text-gray-600">
              {formatTime(recordingTime)}
            </span>
          </div>
        )}
        
        {isProcessing && (
          <div className="text-primary-600 font-medium animate-pulse">
            Processing your message...
          </div>
        )}
        
        {!isRecording && !isProcessing && (
          <div className="text-gray-500 text-sm">
            Click to start speaking
          </div>
        )}
      </div>

      {/* Instructions */}
      {!isRecording && !isProcessing && (
        <div className="text-center text-xs text-gray-400 max-w-xs">
          Speak naturally in {language || 'your preferred language'}. 
          The bot will listen and respond with empathy and support.
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;

