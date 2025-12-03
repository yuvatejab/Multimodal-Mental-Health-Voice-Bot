from fastapi import APIRouter
from .chat_routes import router as chat_router
from .coping_routes import router as coping_router
from .therapist_routes import router as therapist_router

# Create main router
router = APIRouter()

# Include all sub-routers (chat_router already has /api prefix)
router.include_router(chat_router)
router.include_router(coping_router, prefix="/api/coping", tags=["coping"])
router.include_router(therapist_router, prefix="/api/therapists", tags=["therapists"])

__all__ = ["router"]

