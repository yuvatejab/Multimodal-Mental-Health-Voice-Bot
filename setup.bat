@echo off
REM Mental Health Voice Bot - Setup Script for Windows
REM This script sets up both backend and frontend

echo 🎙️ Mental Health Voice Bot - Setup Script
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Check Node version
echo Checking Node.js version...
node --version
echo.

REM Backend setup
echo 📦 Setting up Backend...
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Backend setup complete!
echo.

REM Frontend setup
cd ..\frontend
echo 📦 Setting up Frontend...
echo Installing Node.js dependencies...
call npm install

echo ✅ Frontend setup complete!
echo.

REM Final instructions
cd ..
echo ==========================================
echo ✨ Setup Complete!
echo.
echo Next steps:
echo 1. Get your Groq API key from: https://console.groq.com
echo 2. Edit backend\.env and add your GROQ_API_KEY
echo 3. Run the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 4. In a new terminal, run the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 5. Open http://localhost:5173 in your browser
echo.
echo For detailed instructions, see QUICKSTART.md
echo ==========================================
pause

