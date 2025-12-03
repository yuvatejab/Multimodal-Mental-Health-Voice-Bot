# Mental Health Voice Bot 🎙️💙

A compassionate, voice-first mental health support chatbot with multilingual support, personalized coping strategies, and therapist finder. Built with FastAPI, React, and powered by Groq's ultra-fast AI models.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

## ✨ Features

### 🎤 Voice & Chat
- **Voice-First Experience**: Natural voice conversations with real-time processing
- **Multilingual Support**: 10+ languages including English, Hindi, Spanish, French, German, Portuguese, Italian, Japanese, Korean, and Chinese
- **Emotional Voice**: Natural-sounding responses with subtle emotional prosody
- **Ultra-Fast Inference**: Powered by Groq's LPU for near-instant responses (<2 seconds end-to-end)

### 💡 Coping Strategies
- **22 Evidence-Based Exercises**: Breathing techniques, grounding exercises, mindfulness, CBT, and physical activities
- **Personalized Recommendations**: AI-powered suggestions based on your conversation
- **Video Guides**: YouTube tutorials for each strategy
- **Scientific Backing**: Each strategy includes research references
- **Multilingual**: Available in English and Hindi

### 🏥 Therapist Finder
- **27+ Verified Therapists**: Across 9 major Indian states
- **Smart Search**: Filter by state, specialty, language, price, and availability
- **AI Recommendations**: Get therapist suggestions based on your needs
- **Detailed Profiles**: Ratings, experience, specialties, and contact information
- **Online & In-Person**: Options for both consultation types

### 🚨 Safety & Support
- **Crisis Detection**: Identifies crisis indicators in multiple languages
- **Indian Helplines**: AASRA, Vandrevala Foundation, Kiran, iCall, NIMHANS
- **Culturally Sensitive**: Designed for Indian users with understanding of local context
- **Privacy-Focused**: Conversations are ephemeral with no persistent storage

### 🎨 User Experience
- **Modern UI**: Beautiful, calming interface with smooth animations
- **Mobile Responsive**: Works seamlessly on all devices
- **Easy Navigation**: Intuitive routing between chat, strategies, and therapist finder
- **100% Free**: Uses free APIs (Groq, Edge TTS) with generous limits

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                    │
│  ┌──────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │  Chat Page   │  │ Coping Strategies│  │ Therapist Finder│ │
│  └──────────────┘  └─────────────────┘  └────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │ REST API
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │ STT Service│  │ LLM Service│  │   Therapy Service    │  │
│  │  (Whisper) │  │ (Llama 3.1)│  │  (Crisis Detection)  │  │
│  └────────────┘  └────────────┘  └──────────────────────┘  │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │ TTS Service│  │Emotion Svc │  │   Coping Service     │  │
│  │ (Edge TTS) │  │(Groq LLM)  │  │ (22 Strategies DB)   │  │
│  └────────────┘  └────────────┘  └──────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Therapist Service (27+ Therapists DB)        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    Groq API            Groq API            Edge TTS (Free)
   (Whisper)           (Llama 3.1)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (3.13 recommended)
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
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_groq_api_key_here > .env

# Run the backend
python run.py
```

Backend will start at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Run the frontend
npm run dev
```

Frontend will start at `http://localhost:5173`

### 4. Access the Application

Open your browser and navigate to `http://localhost:5173`

## 📖 Usage Guide

### Voice Chat
1. Click the microphone button to start recording
2. Speak your concerns or questions
3. The bot will transcribe, process, and respond with voice
4. Responses are personalized and empathetic

### Coping Strategies
1. Click the "Coping Strategies" button in the header or chat
2. Browse 22 evidence-based exercises
3. Filter by category (breathing, grounding, mindfulness, CBT, physical)
4. Expand any strategy to see:
   - Step-by-step instructions
   - Video guide
   - Scientific basis
   - External resources

### Find a Therapist
1. Click the "Find a Therapist" button
2. Use filters to search:
   - **State**: Select from 9 major Indian states
   - **Specialty**: Anxiety, depression, trauma, OCD, etc.
   - **Language**: English, Hindi, Tamil, etc.
   - **Max Price**: Set your budget
   - **Online Only**: Filter for virtual consultations
3. View detailed therapist profiles
4. Contact directly via phone or website

### Crisis Support
- If crisis indicators are detected, you'll see prominent help buttons
- Access Indian crisis helplines immediately:
  - **AASRA**: 91-9820466726 (24/7)
  - **Vandrevala Foundation**: 1860-266-2345 (24/7, Free)
  - **Kiran**: 1800-599-0019 (24/7, Toll-free)
  - **iCall**: 022-25521111 (Mon-Sat, 8 AM-10 PM)

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **Groq SDK**: Ultra-fast AI inference (Whisper + Llama 3.1)
- **Edge TTS**: Free, high-quality text-to-speech
- **Python 3.13**: Latest Python with async support

### Frontend
- **React 18**: Modern UI library
- **Vite**: Lightning-fast build tool
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client

### AI Models
- **Whisper Large V3**: Speech-to-text (via Groq)
- **Llama 3.1 8B**: LLM responses (via Groq)
- **Edge TTS**: Text-to-speech (Microsoft)

## 📁 Project Structure

```
mental-health-voice-bot/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Configuration
│   │   ├── data/
│   │   │   ├── coping_strategies.json    # 22 exercises
│   │   │   └── therapists.json           # 27+ therapists
│   │   ├── models/
│   │   │   ├── schemas.py          # Pydantic models
│   │   │   └── emotion_schemas.py  # Emotion detection models
│   │   ├── services/
│   │   │   ├── stt_service.py      # Speech-to-text
│   │   │   ├── llm_service.py      # LLM + crisis detection
│   │   │   ├── tts_service.py      # Text-to-speech
│   │   │   ├── therapy_service.py  # Mental health logic
│   │   │   ├── emotion_service.py  # Emotion detection
│   │   │   ├── coping_service.py   # Coping strategies
│   │   │   └── therapist_service.py # Therapist search
│   │   ├── routes/
│   │   │   ├── chat_routes.py      # Chat API
│   │   │   ├── coping_routes.py    # Coping API
│   │   │   └── therapist_routes.py # Therapist API
│   │   └── utils/
│   │       └── ssml_builder.py     # Voice synthesis utils
│   ├── requirements.txt
│   ├── run.py                      # Server startup script
│   └── .env                        # Environment variables
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ChatPage.jsx        # Main chat interface
│   │   │   ├── CopingStrategiesPage.jsx  # Strategies browser
│   │   │   └── TherapistFinderPage.jsx   # Therapist search
│   │   ├── components/
│   │   │   ├── VoiceRecorder.jsx   # Audio recording
│   │   │   ├── ChatInterface.jsx   # Message display
│   │   │   ├── LanguageSelector.jsx # Language picker
│   │   │   └── ActionButtons.jsx   # Navigation buttons
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── App.jsx                 # Router setup
│   │   └── main.jsx                # Entry point
│   ├── package.json
│   └── vite.config.js
├── README.md
├── QUICKSTART.md
└── .gitignore
```

## 🔧 API Endpoints

### Chat Endpoints
- `POST /api/voice-chat` - Complete voice pipeline (STT → LLM → TTS)
- `POST /api/chat` - Text-only chat
- `POST /api/transcribe` - Speech-to-text only
- `GET /api/languages` - Supported languages
- `GET /api/health` - Health check

### Coping Strategies Endpoints
- `GET /api/coping/personalized` - Get personalized strategies
- `GET /api/coping/all` - Get all strategies (with optional category filter)
- `GET /api/coping/categories` - Get all categories
- `GET /api/coping/strategy/{id}` - Get specific strategy

### Therapist Finder Endpoints
- `GET /api/therapists/search` - Search therapists with filters
- `GET /api/therapists/recommended` - Get AI-recommended therapists
- `GET /api/therapists/states` - Get available states
- `GET /api/therapists/specialties` - Get all specialties
- `GET /api/therapists/therapist/{id}` - Get specific therapist
- `GET /api/therapists/city/{city}` - Get therapists by city

## 🌐 Supported Languages

- 🇬🇧 English
- 🇮🇳 Hindi (हिंदी)
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇵🇹 Portuguese (Português)
- 🇮🇹 Italian (Italiano)
- 🇯🇵 Japanese (日本語)
- 🇰🇷 Korean (한국어)
- 🇨🇳 Chinese (中文)

## 🎯 Key Features Explained

### Emotion Detection
- Analyzes user messages for emotional content
- Detects: anxiety, depression, stress, anger, fear, happiness, etc.
- Adjusts voice prosody (rate, pitch, volume) for empathetic responses
- Identifies crisis situations automatically

### Coping Strategies Database
- **22 Evidence-Based Exercises**:
  - 4-7-8 Breathing, Box Breathing, Alternate Nostril Breathing
  - 5-4-3-2-1 Grounding, Ice Grounding, Sensory Object Grounding
  - Body Scan, Loving-Kindness Meditation, RAIN Technique
  - Thought Record, Worry Time, Problem-Solving
  - Progressive Muscle Relaxation, Yoga, Walking, Stretching
  - And more...
- Each includes: steps, duration, difficulty, videos, scientific basis

### Therapist Database
- **27+ Verified Therapists** across India
- **States Covered**: Maharashtra, Karnataka, Delhi, Tamil Nadu, West Bengal, Gujarat, Rajasthan, Uttar Pradesh, Telangana
- **Specialties**: Anxiety, Depression, Trauma, OCD, Bipolar, Addiction, Child Psychiatry, ADHD, Eating Disorders, and more
- **Verified Credentials**: MD, PhD, RCI registered professionals

## 🚨 Crisis Resources (India)

### 24/7 Helplines
- **AASRA**: 91-9820466726
- **Vandrevala Foundation**: 1860-266-2345 / 1800-2333-330 (Toll-free)
- **Kiran Mental Health**: 1800-599-0019 (Toll-free)

### Daytime Support
- **iCall**: 022-25521111 (Mon-Sat, 8 AM-10 PM)
- **NIMHANS**: 080-46110007 (Mon-Sat, 9 AM-5:30 PM)
- **Fortis Stress Helpline**: 8376804102

## 🔒 Privacy & Security

- **No Data Storage**: Conversations are not saved to databases
- **Session-Based**: Data exists only during your session
- **No User Accounts**: Anonymous usage, no registration required
- **HTTPS Ready**: Production deployment uses SSL/TLS
- **API Key Security**: Environment variables for sensitive data

## 🚀 Deployment

### Render.com (Recommended)

1. **Backend**:
   - Create new Web Service
   - Connect GitHub repository
   - Build: `pip install -r backend/requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add `GROQ_API_KEY` environment variable

2. **Frontend**:
   - Create new Static Site
   - Build: `cd frontend && npm install && npm run build`
   - Publish: `frontend/dist`
   - Add `VITE_API_URL` environment variable

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Additional coping strategies
- More therapist profiles
- Additional language support
- UI/UX improvements
- Bug fixes and optimizations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing ultra-fast AI inference
- **Microsoft Edge TTS**: For free, high-quality text-to-speech
- **Mental Health Professionals**: For guidance on crisis resources
- **Open Source Community**: For the amazing tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mental-health-voice-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mental-health-voice-bot/discussions)

## ⚠️ Disclaimer

This application is a support tool and **NOT a replacement for professional mental health care**. If you're experiencing a mental health crisis, please:

1. Contact emergency services (112 in India)
2. Call a crisis helpline (listed above)
3. Visit the nearest hospital emergency department
4. Reach out to a mental health professional

Always consult with qualified healthcare providers for diagnosis and treatment.

---

**Built for mental health awareness and support**

**Star ⭐ this repo if you find it helpful!**
