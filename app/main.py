from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import log

# CRITICAL: Import engine and Base
from app.db.database import engine
from app.models.base import Base
# CRITICAL: Import your models so Base knows they exist before creating tables
from app.models import admin, feedback 

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A robust backend API for managing user feedback.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    log.info("Application startup initialized.")
    
    # Automatically create tables in SQLite on startup
    log.info("Creating database tables if they do not exist...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("Database tables ready.")