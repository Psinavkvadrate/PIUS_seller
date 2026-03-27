import uuid
from sqlalchemy import Column, String, Boolean, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    userId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, unique=True, nullable=False, index=True)
    passwordHash = Column(String, nullable=False)

    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    patronymic = Column(String)

    dateOfBirth = Column(Date, nullable=False)
    city = Column(String, nullable=False)

    telegram = Column(String)
    telegramChatId = Column(String)

    isSeller = Column(Boolean, default=False, index=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())

    markets = relationship("Market", back_populates="owner")

    tokens = relationship("UserToken", back_populates="user")