# Backend - Mental Health Voice Bot

FastAPI backend for the Mental Health Voice Bot application.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp ../.env.example .env
```

4. Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_actual_api_key_here
```

## Running

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Get supported languages
curl http://localhost:8000/api/languages
```

