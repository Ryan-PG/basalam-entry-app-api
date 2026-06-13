from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.feedbacks import router as feedback_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(feedback_router, prefix="/feedbacks", tags=["Feedbacks"])