import uuid  # 1. Make sure uuid is imported at the top!
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from app.db.database import get_db
from app.core.config import settings
from app.models.admin import Admin
from app.repositories.admin import AdminRepository
from app.schemas.token import TokenPayload

security = HTTPBearer()

async def get_current_admin(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Admin:
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token payload")
        
        admin_id = uuid.UUID(token_data.sub)
        
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    repo = AdminRepository(Admin, db)
    
    admin = await repo.get(admin_id) 
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin