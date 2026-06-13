import uuid
from datetime import datetime, timezone
import enum
from sqlalchemy import String, Text, DateTime, Enum, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class FeedbackStatus(str, enum.Enum):
    submitted = "submitted"
    under_review = "under_review"
    resolved = "resolved"

class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), index=True)
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[FeedbackStatus] = mapped_column(Enum(FeedbackStatus), default=FeedbackStatus.submitted, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))