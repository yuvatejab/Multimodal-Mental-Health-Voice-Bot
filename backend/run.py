"""
Run script for the Mental Health Voice Bot backend.
This runs uvicorn without watching the venv directory to avoid reload issues.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],  # Only watch the app directory, not venv
        log_level="info"
    )

