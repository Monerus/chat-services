from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Group(Base):
    __tablename__ = "group"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    created_user: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    avatar_url: Mapped[str] = mapped_column(String(300), nullable=True)
    
    description: Mapped[str] = mapped_column(String(150), nullable=True)


