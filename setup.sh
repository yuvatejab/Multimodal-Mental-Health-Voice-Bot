#!/bin/bash

# Mental Health Voice Bot - Setup Script
# This script sets up both backend and frontend

echo "🎙️ Mental Health Voice Bot - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check Node version
echo "Checking Node.js version..."
node_version=$(node --version 2>&1)
echo "Found Node.js $node_version"
echo ""

# Backend setup
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend setup
cd ../frontend
echo "📦 Setting up Frontend..."
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

# Final instructions
cd ..
echo "=========================================="
echo "✨ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Get your Groq API key from: https://console.groq.com"
echo "2. Edit backend/.env and add your GROQ_API_KEY"
echo "3. Run the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "4. In a new terminal, run the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "5. Open http://localhost:5173 in your browser"
echo ""
echo "For detailed instructions, see QUICKSTART.md"
echo "=========================================="

