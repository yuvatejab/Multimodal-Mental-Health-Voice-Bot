# Quick Start Guide 🚀

Get the Mental Health Voice Bot running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- A Groq API key (free from [console.groq.com](https://console.groq.com))

## Step 1: Get Your Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to "API Keys" section
4. Click "Create API Key"
5. Copy your API key (you'll need it in Step 3)

## Step 2: Install Dependencies

### Backend
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Step 3: Configure Environment Variables

### Backend
Edit `backend/.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```

### Frontend
The `frontend/.env` file is already configured for local development. No changes needed!

## Step 4: Run the Application

Open **two terminal windows**:

### Terminal 1 - Backend
```bash
cd backend
# Activate virtual environment if not already activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

## Step 5: Open the Application

Open your browser and go to: **http://localhost:5173**

## Step 6: Test It Out!

1. Click the microphone button
2. Allow microphone access when prompted
3. Speak naturally (e.g., "I'm feeling a bit stressed today")
4. Click the microphone button again to stop recording
5. Wait a few seconds for the AI to respond with voice!

## Troubleshooting

### "GROQ_API_KEY is not set"
- Make sure you edited `backend/.env` and added your API key
- Restart the backend server after adding the key

### "Could not access microphone"
- Click the browser's address bar and check microphone permissions
- Make sure no other application is using your microphone

### "Unable to connect to the server"
- Make sure the backend is running on port 8000
- Check that you're accessing the frontend at http://localhost:5173

### Backend won't start
- Make sure you activated the virtual environment
- Try: `pip install --upgrade pip` then `pip install -r requirements.txt` again

### Frontend won't start
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

## What's Next?

- Try different languages using the language selector
- Read the full [README.md](README.md) for more features
- Check [DEPLOYMENT.md](DEPLOYMENT.md) to deploy your bot online
- Customize the system prompt in `backend/app/services/llm_service.py`

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Look at the API documentation: http://localhost:8000/docs
- Open an issue on GitHub

---

**Enjoy your Mental Health Voice Bot! 💙**

