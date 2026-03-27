from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.async_session import AsyncSessionLocal, get_async_db
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.controllers.auth_controller import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_async_db)):
    user, result = await register_user(db, request)
    if not user:
        return {"success": False, "message": result}
    return {
        "success": True,
        "user": {
            "userId": user.userId,
            "login": user.login,
            "firstName": user.firstName,
            "isSeller": user.isSeller
        },
        "token": result
    }

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    user, result = await login_user(db, request)
    if not user:
        return {"success": False, "message": result}
    return {
        "success": True,
        "user": {
            "userId": user.userId,
            "login": user.login,
            "firstName": user.firstName,
            "isSeller": user.isSeller
        },
        "token": result
    }