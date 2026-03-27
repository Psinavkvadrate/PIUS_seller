import uuid
from sqlalchemy import Column, String, Boolean, Date, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.base import Base


class User(Base):

    __tablename__ = "users"

    userId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    login = Column(String, unique=True, nullable=False)

    passwordHash = Column(String, nullable=False)

    firstName = Column(String)

    lastName = Column(String)

    patronymic = Column(String)

    dateOfBirth = Column(Date)

    city = Column(String)

    telegram = Column(String)

    telegramChatId = Column(String)

    isSeller = Column(Boolean, default=False)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_user_isSeller", "isSeller"),
    )