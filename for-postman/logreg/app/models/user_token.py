import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserToken(Base):
    __tablename__ = "user_tokens"

    tokenId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    userId = Column(UUID(as_uuid=True), ForeignKey("users.userId"), nullable=False)

    token = Column(String, nullable=False)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    expiresAt = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")