# Mental Health Voice Bot 🎙️💙

A compassionate, voice-first mental health support chatbot with multilingual support. Built with FastAPI, React, and powered by Groq's ultra-fast AI models.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

## ✨ Features

- 🎤 **Voice-First Experience**: Natural voice conversations with real-time processing
- 🌍 **Multilingual Support**: 10+ languages including English, Hindi, Spanish, French, German, Portuguese, Italian, Japanese, Korean, and Chinese
- ⚡ **Ultra-Fast Inference**: Powered by Groq's LPU for near-instant responses (<2 seconds end-to-end)
- 🔒 **Privacy-Focused**: Conversations are ephemeral with no persistent storage
- 🎨 **Modern UI**: Beautiful, calming interface with smooth animations
- 🚨 **Crisis Detection**: Identifies crisis indicators and provides appropriate resources
- 🆓 **100% Free**: Uses free APIs (Groq, Edge TTS) with generous limits

## 🏗️ Architecture

```
┌─────────────────┐
│   React Frontend │
│   (Vite + Tailwind) │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│  FastAPI Backend │
│  ┌────────────┐ │
│  │ STT Service│ │  ← Groq Whisper
│  │ LLM Service│ │  ← Groq Llama 3.1
│  │ TTS Service│ │  ← Edge TTS
│  │ Therapy Svc│ │
│  └────────────┘ │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Groq API key (free from [console.groq.com](https://console.groq.com))

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd mental-health-voice-bot
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_api_key_here
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# The default settings should work for local development
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
# Make sure virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
mental-health-voice-bot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config.py            # Configuration and settings
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── services/
│   │   │   ├── stt_service.py   # Speech-to-text (Groq Whisper)
│   │   │   ├── llm_service.py   # LLM responses (Groq Llama)
│   │   │   ├── tts_service.py   # Text-to-speech (Edge TTS)
│   │   │   └── therapy_service.py # Mental health logic
│   │   └── routes/
│   │       └── chat_routes.py   # API endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceRecorder.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   └── LanguageSelector.jsx
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── .gitignore
├── render.yaml                   # Render.com deployment config
└── README.md
```

## 🌐 API Endpoints

### Health Check
```
GET /api/health
```

### Get Supported Languages
```
GET /api/languages
```

### Voice Chat (Complete Pipeline)
```
POST /api/voice-chat
Content-Type: multipart/form-data

Parameters:
- audio: Audio file (webm, mp3, wav)
- language: Language code (optional)
- session_id: Session identifier (optional)
```

### Text Chat
```
POST /api/chat
Content-Type: application/json

Body:
{
  "message": "I'm feeling anxious today",
  "language": "en",
  "conversation_history": []
}
```

### Transcribe Audio
```
POST /api/transcribe
Content-Type: multipart/form-data

Parameters:
- audio: Audio file
- language: Language code
```

## 🚢 Deployment

### Deploy to Render.com (Recommended - Free Tier)

1. **Push your code to GitHub**

2. **Sign up at [Render.com](https://render.com)**

3. **Create a new Blueprint**
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

4. **Add Environment Variables**
   - In the backend service settings, add:
     - `GROQ_API_KEY`: Your Groq API key

5. **Deploy**
   - Render will automatically build and deploy both services
   - Frontend URL: `https://mental-health-voice-bot-frontend.onrender.com`
   - Backend URL: `https://mental-health-voice-bot-backend.onrender.com`

### Alternative: Deploy to Vercel (Frontend) + Render (Backend)

**Backend on Render:**
```bash
# Same as above for backend
```

**Frontend on Vercel:**
```bash
cd frontend
npm install -g vercel
vercel

# Set environment variable:
# VITE_API_URL=https://your-backend-url.onrender.com
```

## 🔑 Getting API Keys

### Groq API Key (Required)
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and add to your `.env` file

**Free Tier Limits:**
- 14,400 requests per day
- 500+ tokens/second
- More than enough for personal projects and portfolios

## 🎨 Customization

### Adding New Languages

Edit `backend/app/config.py`:
```python
SUPPORTED_LANGUAGES: dict = {
    "your_lang_code": {
        "name": "Language Name",
        "voice": "edge-tts-voice-code"
    }
}
```

Find Edge TTS voices: [Edge TTS Voice List](https://github.com/rany2/edge-tts#voice-list)

### Customizing the System Prompt

Edit `backend/app/services/llm_service.py` - modify the `system_prompt` variable.

### Changing UI Colors

Edit `frontend/tailwind.config.js` to customize the color scheme.

## 🧪 Testing

### Manual Testing Checklist

- [ ] Record voice message in English
- [ ] Test different languages (Hindi, Spanish, etc.)
- [ ] Verify audio playback works
- [ ] Test crisis keyword detection
- [ ] Check mobile responsiveness
- [ ] Verify conversation history
- [ ] Test clear conversation feature

### Testing Crisis Detection

Try phrases like:
- "I'm feeling suicidal"
- "I want to hurt myself"

The bot should respond with crisis resources.

## 🛠️ Troubleshooting

### Backend Issues

**"GROQ_API_KEY is not set"**
- Make sure you created a `.env` file in the backend directory
- Verify the API key is correctly formatted

**"Could not access microphone"**
- Check browser permissions
- Use HTTPS in production (required for microphone access)

**"Error transcribing audio"**
- Verify your Groq API key is valid
- Check your internet connection
- Ensure audio file is not corrupted

### Frontend Issues

**"Unable to connect to the server"**
- Make sure backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env`
- Verify CORS settings in `backend/app/config.py`

**Audio not playing**
- Check browser console for errors
- Verify audio format is supported
- Try a different browser

## 📊 Performance

- **Speech-to-Text**: ~0.5-1 second (Groq Whisper)
- **LLM Response**: ~0.5-1 second (Groq Llama 3.1)
- **Text-to-Speech**: ~1-2 seconds (Edge TTS)
- **Total Pipeline**: ~2-4 seconds end-to-end

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Important Disclaimer

This application is a support tool and **NOT a replacement for professional mental health care**. If you or someone you know is in crisis, please contact:

- **US**: National Suicide Prevention Lifeline: 988
- **US**: Crisis Text Line: Text HOME to 741741
- **International**: [IASP Crisis Centers](https://www.iasp.info/resources/Crisis_Centres/)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for ultra-fast AI inference
- [Edge TTS](https://github.com/rany2/edge-tts) for free text-to-speech
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://react.dev/) and [Vite](https://vitejs.dev/) for the frontend
- [Tailwind CSS](https://tailwindcss.com/) for styling

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for mental health awareness and support**

