from pydantic import BaseModel
from datetime import date
from uuid import UUID
from typing import Optional


class RegisterRequest(BaseModel):
    login: str
    password: str
    firstName: str
    lastName: str
    patronymic: Optional[str]
    dateOfBirth: date
    city: str
    telegram: Optional[str]
    isSeller: bool


class LoginRequest(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    userId: UUID
    login: str
    firstName: str
    isSeller: bool


class AuthResponse(BaseModel):
    success: bool
    user: Optional[UserResponse] = None
    token: Optional[str] = None
    message: Optional[str] = None