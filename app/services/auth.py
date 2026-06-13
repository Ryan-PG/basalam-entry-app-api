from app.models.admin import Admin
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.admin import AdminCreate, AdminLogin
from app.repositories.admin import AdminRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.logger import log

class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = AdminRepository(Admin, session)

    async def register_admin(self, admin_in: AdminCreate):
        if await self.repo.get_by_email(admin_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_obj = await self.repo.create({
            "username": admin_in.username,
            "email": admin_in.email,
            "password_hash": get_password_hash(admin_in.password)
        })
        log.info(f"New admin registered: {db_obj.email}")
        return db_obj

    async def authenticate(self, admin_in: AdminLogin):
        admin = await self.repo.get_by_email(admin_in.email)
        if not admin or not verify_password(admin_in.password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        
        access_token = create_access_token(subject=str(admin.id))
        log.info(f"Admin logged in: {admin.email}")
        return {"access_token": access_token, "token_type": "bearer"}