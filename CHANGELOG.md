# Changelog

All notable changes to the Mental Health Voice Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-03

### Added
- Initial release of Mental Health Voice Bot
- Voice-first conversation interface with real-time recording
- Speech-to-text using Groq Whisper API
- LLM responses using Groq Llama 3.1 8B
- Text-to-speech using Edge TTS
- Support for 10 languages: English, Hindi, Spanish, French, German, Portuguese, Italian, Japanese, Korean, Chinese
- Crisis detection with appropriate resource recommendations
- Modern, responsive UI with Tailwind CSS
- Conversation history management
- Session-based context tracking
- FastAPI backend with clean architecture
- React frontend with Vite
- Comprehensive documentation (README, QUICKSTART, DEPLOYMENT, TESTING)
- Deployment configuration for Render.com
- Docker support
- Setup scripts for Windows and Unix systems

### Features
- Real-time voice recording with visual feedback
- Automatic audio playback of responses
- Language selector with 10+ languages
- Crisis keyword detection
- Empathetic AI responses
- Clean, calming UI design
- Mobile-responsive layout
- Conversation clearing
- Health check endpoints
- API documentation with Swagger UI

### Technical
- FastAPI backend with async/await
- Groq API integration for ultra-fast inference
- Edge TTS for free, high-quality speech synthesis
- Pydantic models for data validation
- CORS configuration for cross-origin requests
- Environment-based configuration
- Modular service architecture
- Component-based React frontend
- Tailwind CSS for styling
- Axios for API communication

### Documentation
- Comprehensive README with setup instructions
- Quick start guide for 5-minute setup
- Detailed deployment guide for multiple platforms
- Testing guide with manual and automated test cases
- Contributing guidelines
- License (MIT)
- Changelog

### Security
- API key protection
- No persistent storage of conversations
- HTTPS requirement for production
- Input validation
- Error handling

## [Unreleased]

### Planned Features
- User authentication
- Conversation export
- Dark mode
- More language support
- Voice activity detection
- Mood tracking
- Conversation analytics
- Text-only mode option
- Keyboard shortcuts
- Admin dashboard

### Known Issues
- Free tier services on Render.com spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Audio playback may not work on older browsers

---

For more details on each release, see the [GitHub Releases](https://github.com/yourusername/mental-health-voice-bot/releases) page.

