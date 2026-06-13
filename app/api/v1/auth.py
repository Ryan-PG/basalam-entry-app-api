from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.admin import AdminCreate, AdminResponse, AdminLogin
from app.schemas.token import Token
from app.services.auth import AuthService

router = APIRouter()

@router.post("/register", response_model=AdminResponse, status_code=201)
async def register(admin_in: AdminCreate, db: AsyncSession = Depends(get_db)):
    """Register a new admin user."""
    return await AuthService(db).register_admin(admin_in)

@router.post("/login", response_model=Token)
async def login(admin_in: AdminLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate admin and return JWT."""
    return await AuthService(db).authenticate(admin_in)