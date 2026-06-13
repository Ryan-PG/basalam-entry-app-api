from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackUpdateStatus
from app.services.feedback import FeedbackService
from app.models.feedback import FeedbackStatus
from app.api.deps import get_current_admin
from app.models.admin import Admin
import uuid

router = APIRouter()

@router.post("", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(feedback_in: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """Public endpoint to submit feedback."""
    return await FeedbackService(db).create_feedback(feedback_in)

@router.get("", response_model=list[FeedbackResponse])
async def list_feedbacks(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: FeedbackStatus | None = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Admin endpoint to list feedbacks."""
    return await FeedbackService(db).get_feedbacks(page, size, status)

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Admin endpoint to view feedback details."""
    return await FeedbackService(db).get_feedback(feedback_id)

@router.patch("/{feedback_id}/status", response_model=FeedbackResponse)
async def update_status(
    feedback_id: uuid.UUID,
    status_update: FeedbackUpdateStatus,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Admin endpoint to update feedback status."""
    return await FeedbackService(db).update_feedback_status(feedback_id, status_update)