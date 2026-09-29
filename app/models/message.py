from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda:str(uuid4()),  
        )

class Message(Base):
    __tablename__ = "message"

    content: Mapped[str] = mapped_column(String(150), nullable=True)

    sender_id: Mapped[str] = mapped_column(nullable=False)

    receiver_id: Mapped[str] = mapped_column(nullable=False)

    image_key: Mapped[str] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
