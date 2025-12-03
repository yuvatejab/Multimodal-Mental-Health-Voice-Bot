# Testing Guide

This guide covers testing the Mental Health Voice Bot application.

## Manual Testing

### 1. Backend API Testing

#### Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Mental Health Voice Bot API is running"
}
```

#### Get Languages
```bash
curl http://localhost:8000/api/languages
```

Expected: List of supported languages with codes and voice names.

#### Text Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling anxious today",
    "language": "en"
  }'
```

Expected: JSON response with empathetic text response.

### 2. Frontend Testing

#### Voice Recording
1. Open http://localhost:5173
2. Click the microphone button
3. Allow microphone access
4. Speak a message (e.g., "Hello, I need someone to talk to")
5. Click the microphone button again to stop
6. Verify:
   - Recording timer shows during recording
   - "Processing" message appears
   - User message appears in chat
   - Bot response appears with audio icon
   - Audio plays automatically

#### Language Selection
1. Click the language selector (globe icon)
2. Select a different language (e.g., Spanish)
3. Record a message in that language
4. Verify:
   - Transcription is in the selected language
   - Response is in the selected language
   - Audio is in the selected language

#### Audio Playback
1. After receiving a bot response
2. Click the "Play audio" button
3. Verify audio plays correctly
4. Try playing multiple messages

#### Crisis Detection
1. Record or type a message with crisis keywords:
   - "I want to hurt myself"
   - "I'm thinking about suicide"
2. Verify:
   - Crisis warning banner appears
   - Response includes crisis resources
   - Appropriate helpline numbers are shown

### 3. Multi-Language Testing

Test with these sample phrases:

**English:**
- "I'm feeling stressed about work"
- "Can you help me with my anxiety?"

**Hindi:**
- "मैं बहुत परेशान हूं" (I am very worried)
- "मुझे मदद चाहिए" (I need help)

**Spanish:**
- "Me siento muy ansioso" (I feel very anxious)
- "Necesito hablar con alguien" (I need to talk to someone)

**French:**
- "Je me sens déprimé" (I feel depressed)
- "J'ai besoin d'aide" (I need help)

### 4. UI/UX Testing

#### Responsive Design
1. Open browser developer tools
2. Test different screen sizes:
   - Mobile (375px width)
   - Tablet (768px width)
   - Desktop (1920px width)
3. Verify:
   - Layout adapts properly
   - All buttons are accessible
   - Text is readable
   - No horizontal scrolling

#### Animations
1. Verify smooth animations:
   - Message slide-up effect
   - Recording pulse animation
   - Button hover effects
   - Dropdown transitions

#### Accessibility
1. Test keyboard navigation:
   - Tab through all interactive elements
   - Press Enter to activate buttons
   - Press Escape to close dropdowns
2. Verify ARIA labels are present
3. Check color contrast ratios

### 5. Error Handling

#### Network Errors
1. Stop the backend server
2. Try recording a message
3. Verify:
   - Error message appears
   - User is informed gracefully
   - Application doesn't crash

#### Invalid Audio
1. Try uploading a very short audio clip (<0.5 seconds)
2. Verify error handling

#### API Key Issues
1. Set invalid GROQ_API_KEY in backend
2. Restart backend
3. Try recording a message
4. Verify appropriate error message

### 6. Performance Testing

#### Response Time
Measure end-to-end latency:
1. Start recording
2. Speak for 3-5 seconds
3. Stop recording
4. Measure time until audio response plays

Target: <4 seconds total

#### Concurrent Users
1. Open multiple browser tabs
2. Use the application simultaneously
3. Verify no conflicts or errors

### 7. Browser Compatibility

Test on:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

### 8. Security Testing

#### HTTPS Requirement
1. Try accessing via HTTP in production
2. Verify microphone access is blocked (expected)
3. Confirm HTTPS is required

#### API Key Protection
1. Inspect network requests in browser
2. Verify API key is never exposed to frontend
3. Check that .env file is in .gitignore

### 9. Session Management

#### Conversation Context
1. Have a multi-turn conversation
2. Verify bot remembers context
3. Test with 5+ messages
4. Verify conversation history is maintained

#### Clear Conversation
1. Have a conversation
2. Click the refresh/clear button
3. Verify:
   - Messages are cleared
   - New session is created
   - Next conversation starts fresh

### 10. Edge Cases

#### Very Long Messages
1. Record a 30+ second message
2. Verify it processes correctly

#### Silence
1. Record without speaking
2. Verify appropriate handling

#### Background Noise
1. Record with background music/noise
2. Verify transcription quality

#### Multiple Languages in One Message
1. Speak in mixed languages
2. Observe how it's handled

## Automated Testing (Future)

### Backend Unit Tests
```python
# Example test structure
import pytest
from app.services.llm_service import LLMService

@pytest.mark.asyncio
async def test_crisis_detection():
    llm_service = LLMService()
    result = await llm_service.detect_crisis("I want to hurt myself")
    assert result == True
```

### Frontend Unit Tests
```javascript
// Example test structure
import { render, screen } from '@testing-library/react';
import VoiceRecorder from './components/VoiceRecorder';

test('renders record button', () => {
  render(<VoiceRecorder />);
  const button = screen.getByRole('button');
  expect(button).toBeInTheDocument();
});
```

## Test Checklist

Before deploying:

- [ ] All API endpoints return correct responses
- [ ] Voice recording works in all supported browsers
- [ ] All languages transcribe correctly
- [ ] Audio playback works
- [ ] Crisis detection triggers appropriately
- [ ] UI is responsive on mobile
- [ ] Error messages are user-friendly
- [ ] Performance meets targets (<4s end-to-end)
- [ ] No console errors
- [ ] HTTPS works in production
- [ ] Environment variables are properly set
- [ ] .env files are not committed to git

## Reporting Issues

When reporting a bug, include:
1. Browser and version
2. Operating system
3. Steps to reproduce
4. Expected behavior
5. Actual behavior
6. Console errors (if any)
7. Network errors (if any)

## Performance Benchmarks

Target metrics:
- Speech-to-Text: <1 second
- LLM Response: <1 second  
- Text-to-Speech: <2 seconds
- Total Pipeline: <4 seconds
- UI Response: <100ms
- Page Load: <2 seconds

## Load Testing

For production deployment:
```bash
# Install Apache Bench
# Test API endpoint
ab -n 100 -c 10 http://localhost:8000/api/health

# Expected: 100% success rate
```

## Monitoring

In production, monitor:
- API response times
- Error rates
- Groq API usage
- Server resource usage
- User session duration
- Most common languages used
- Crisis detection frequency

## Continuous Testing

Set up:
1. GitHub Actions for automated tests
2. Pre-commit hooks for linting
3. Staging environment for testing before production
4. User feedback collection
5. Error tracking (e.g., Sentry)

