from sqlalchemy import select
from app.models.admin import Admin
from app.repositories.base import BaseRepository

class AdminRepository(BaseRepository[Admin]):
    async def get_by_email(self, email: str) -> Admin | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()