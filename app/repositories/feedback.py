from sqlalchemy import select, desc
from app.models.feedback import Feedback, FeedbackStatus
from app.repositories.base import BaseRepository

class FeedbackRepository(BaseRepository[Feedback]):
    async def get_multi(self, skip: int = 0, limit: int = 20, status: FeedbackStatus | None = None):
        stmt = select(self.model)
        if status:
            stmt = stmt.where(self.model.status == status)
        stmt = stmt.order_by(desc(self.model.created_at)).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(self, db_obj: Feedback, status: FeedbackStatus) -> Feedback:
        db_obj.status = status
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj