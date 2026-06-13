from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.feedback import FeedbackCreate, FeedbackUpdateStatus
from app.repositories.feedback import FeedbackRepository
from app.models.feedback import Feedback, FeedbackStatus
from app.core.logger import log

class FeedbackService:
    def __init__(self, session: AsyncSession):
        self.repo = FeedbackRepository(Feedback, session)

    async def create_feedback(self, feedback_in: FeedbackCreate):
        feedback = await self.repo.create(feedback_in.model_dump())
        log.info(f"New feedback submitted: {feedback.id}")
        return feedback

    async def get_feedbacks(self, page: int, size: int, status: FeedbackStatus | None):
        skip = (page - 1) * size
        return await self.repo.get_multi(skip=skip, limit=size, status=status)

    async def get_feedback(self, feedback_id: str):
        feedback = await self.repo.get(feedback_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return feedback

    async def update_feedback_status(self, feedback_id: str, status_update: FeedbackUpdateStatus):
        feedback = await self.get_feedback(feedback_id)
        updated_feedback = await self.repo.update_status(feedback, status_update.status)
        log.info(f"Feedback {feedback.id} status updated to {status_update.status}")
        return updated_feedback