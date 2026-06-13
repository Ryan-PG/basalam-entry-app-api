from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from app.models.feedback import FeedbackStatus

class FeedbackCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=5, max_length=5000)

class FeedbackUpdateStatus(BaseModel):
    status: FeedbackStatus

class FeedbackResponse(BaseModel):
    id: UUID
    title: str
    message: str
    status: FeedbackStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)