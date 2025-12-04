# Mental Health Voice Bot 🎙️💙

A compassionate, voice-first mental health support chatbot with multilingual support, personalized coping strategies, therapist finder, and **life-saving emergency contact system**. Built with FastAPI, React, and powered by Groq's ultra-fast AI models.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

## 🌟 Highlights

- 🎤 **Voice-First**: Natural conversations in 10+ languages
- 🆘 **Emergency Alerts**: One-click WhatsApp/SMS to trusted contacts with location
- 💡 **22 Coping Strategies**: Evidence-based exercises with video guides
- 🏥 **27+ Therapists**: Verified professionals across India
- 🚀 **Ultra-Fast**: <2 second response time with Groq's LPU
- 💯 **100% Free**: Uses free APIs (Groq, Edge TTS)

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
- **Emergency Contact System**: Save 1-3 trusted contacts for instant crisis alerts
- **One-Click SOS**: Send emergency alerts via WhatsApp & SMS with location and crisis context
- **Indian Helplines**: AASRA, Vandrevala Foundation, Kiran, iCall, NIMHANS
- **Location Sharing**: Share your real-time location with emergency contacts during crisis
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
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Emergency Setup & Alert Button (SOS)                │  │
│  └──────────────────────────────────────────────────────┘  │
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
│  ┌────────────────────────┐  ┌──────────────────────────┐  │
│  │  Therapist Service     │  │  Emergency Message Svc   │  │
│  │  (27+ Therapists DB)   │  │  (WhatsApp/SMS via      │  │
│  │                        │  │   Twilio)               │  │
│  └────────────────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    Groq API            Groq API            Edge TTS (Free)
   (Whisper)           (Llama 3.1)         Twilio API (Optional)
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
venv\Scripts\python.exe run.py
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

### 🆘 Emergency Contact System

The Emergency Contact System is a life-saving feature that allows you to instantly alert trusted contacts during a mental health crisis.

#### Setup (First-Time Users)
1. When you first use the app, you'll be prompted to set up emergency contacts
2. Add 1-3 trusted contacts with:
   - Name and relationship (Family, Friend, Partner, Therapist, Other)
   - Phone number with country code (e.g., +919876543210)
   - WhatsApp preference (optional)
3. Grant location permission (optional but recommended)
4. Save and continue

#### Using the Emergency Alert
1. **Red SOS Button**: A floating red alert button appears in the bottom-right corner (only visible after setup)
2. **One-Click Alert**: Click the button to send emergency messages to all your contacts
3. **What Gets Sent**:
   - Your current location (with Google Maps link)
   - Your mental health status and recent concerns
   - Crisis helpline numbers
   - Timestamp of the alert
4. **Delivery Methods**:
   - WhatsApp messages (if enabled)
   - SMS messages (as backup)
   - Both methods are tried for maximum reliability

#### Message Example
```
🚨 URGENT: [Your Name] needs help!

Mental State: Distress
Concerns: [Recent conversation context]

📍 Location:
Lat: 19.076090, Lng: 72.877426
https://maps.google.com/?q=19.076090,72.877426

🆘 Immediate Help:
• AASRA: 9820466726
• Vandrevala: 1860-2662-345
• iCall: 9152987821
• NIMHANS: 080-46110007

Please reach out to them immediately.
```

#### Configuration (Twilio Setup)

The system supports two modes:

**1. Simulation Mode (Default - No Setup Required)**
- Messages are logged to backend console
- Perfect for testing and development
- No costs, no external dependencies

**2. Production Mode (WhatsApp & SMS via Twilio)**

To enable actual message delivery:

1. **Sign up for Twilio** (free trial with $15 credit)
   - Visit: https://www.twilio.com/try-twilio
   - Verify your phone number
   - Get your Account SID and Auth Token

2. **Install Twilio SDK**:
   ```bash
   cd backend
   pip install twilio>=9.0.0
   ```

3. **Configure credentials** in `backend/.env`:
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   # Optional: For SMS backup (requires separate Twilio phone number)
   TWILIO_PHONE_NUMBER=+1234567890
   ```

4. **WhatsApp Setup** (Required for trial):
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Send the join code from your phone to activate WhatsApp sandbox
   - Emergency contacts must also join the sandbox

5. **Verify Phone Numbers** (Trial accounts only):
   - Go to: https://console.twilio.com/ → Phone Numbers → Verified Caller IDs
   - Add and verify each emergency contact's phone number

6. **Restart the backend server**

**Important Notes:**
- ✅ **WhatsApp works immediately** after sandbox setup (primary delivery method)
- ⚠️ **SMS is optional** - requires a separate Twilio phone number (not the WhatsApp number)
- 💰 **Costs**: WhatsApp ~$0.005/msg, SMS ~$0.0075/msg (free trial: $15 credit = ~2000 messages)
- 🔒 **Trial Limitations**: Can only send to verified numbers, messages include trial prefix
- 🚀 **Production**: Upgrade account to send to any number without verification

#### Quick Start (Testing Without Twilio)

Want to test the Emergency Contact System without setting up Twilio?

1. **Start the application** (backend + frontend)
2. **Set up emergency contacts** in the app (use any phone number format)
3. **Click the red SOS button**
4. **Check backend terminal** - you'll see simulated messages:
   ```
   [SIMULATED] WhatsApp to +919876543210: 🚨 URGENT: User needs help!
   [SIMULATED] SMS to +919876543210: 🚨 URGENT: User needs help!
   ```

This lets you test the complete flow without any external dependencies!

#### Privacy & Safety
- Emergency contacts are stored locally per session
- No data is sent to external servers (except Twilio when configured)
- You can update or delete contacts anytime
- Location is only shared when you trigger an alert
- All messages include crisis helpline numbers
- WhatsApp is the primary delivery method (SMS is optional backup)

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **Groq SDK**: Ultra-fast AI inference (Whisper + Llama 3.1)
- **Edge TTS**: Free, high-quality text-to-speech
- **Twilio API**: WhatsApp & SMS emergency alerts (optional)
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
│   │   │   ├── therapists.json           # 27+ therapists
│   │   │   └── emergency_contacts.json   # Emergency contacts storage
│   │   ├── models/
│   │   │   ├── schemas.py                # Pydantic models
│   │   │   ├── emotion_schemas.py        # Emotion detection models
│   │   │   └── emergency_schemas.py      # Emergency contact models
│   │   ├── services/
│   │   │   ├── stt_service.py            # Speech-to-text
│   │   │   ├── llm_service.py            # LLM + crisis detection
│   │   │   ├── tts_service.py            # Text-to-speech
│   │   │   ├── therapy_service.py        # Mental health logic
│   │   │   ├── emotion_service.py        # Emotion detection
│   │   │   ├── coping_service.py         # Coping strategies
│   │   │   ├── therapist_service.py      # Therapist search
│   │   │   ├── emergency_storage.py      # Emergency contact storage
│   │   │   └── emergency_message_service.py # WhatsApp/SMS alerts
│   │   ├── routes/
│   │   │   ├── chat_routes.py            # Chat API
│   │   │   ├── coping_routes.py          # Coping API
│   │   │   ├── therapist_routes.py       # Therapist API
│   │   │   └── emergency_routes.py       # Emergency contact API
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
│   │   │   ├── VoiceRecorder.jsx         # Audio recording
│   │   │   ├── ChatInterface.jsx         # Message display
│   │   │   ├── LanguageSelector.jsx      # Language picker
│   │   │   ├── ActionButtons.jsx         # Navigation buttons
│   │   │   ├── EmergencySetup.jsx        # Emergency contact setup
│   │   │   └── EmergencyAlertButton.jsx  # SOS alert button
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

## 🔧 Troubleshooting

### Emergency Contact System

**Issue: "No module named 'twilio'"**
```bash
cd backend
pip install twilio>=9.0.0
```

**Issue: "Mismatch between the 'From' number"**
- This means you're using the WhatsApp number for SMS
- Solution: Either get a separate Twilio SMS number or remove `TWILIO_PHONE_NUMBER` from `.env`
- WhatsApp will still work perfectly!

**Issue: WhatsApp messages not received**
- **Trial accounts**: Verify the recipient's phone number in Twilio Console
- **WhatsApp Sandbox**: Recipient must join by sending the code to Twilio's WhatsApp number
- Check backend logs for detailed error messages

**Issue: Messages show as "SIMULATED"**
- This is normal! It means Twilio is not configured
- Messages are logged to console for testing
- To enable real messages, add Twilio credentials to `backend/.env`

### Backend Issues

**Issue: "Extra inputs are not permitted"**
- Update `backend/app/config.py` to include Twilio fields in the Settings class
- See the configuration section above

**Issue: Backend won't start**
- Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- Install dependencies: `pip install -r requirements.txt`
- Check that `GROQ_API_KEY` is set in `.env`

### Frontend Issues

**Issue: "Cannot connect to backend"**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend/app/config.py`
- Verify API URL in frontend code

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Additional coping strategies
- More therapist profiles
- Additional language support
- UI/UX improvements
- Bug fixes and optimizations
- Alternative messaging providers (Telegram, Discord, etc.)

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
