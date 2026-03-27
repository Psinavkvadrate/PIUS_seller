from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.market import Market
from app.models.user_token import UserToken
from app.core.security import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:

    @staticmethod
    async def register(db: AsyncSession, request):
        existing_user = await UserRepository.get_by_login(db, request.login)
        if existing_user:
            return None, "Login already exists"

        user = User(
            login=request.login,
            passwordHash=hash_password(request.password),
            firstName=request.firstName,
            lastName=request.lastName,
            patronymic=request.patronymic,
            dateOfBirth=request.dateOfBirth,
            city=request.city,
            telegram=request.telegram,
            isSeller=request.isSeller
        )
        user = await UserRepository.create_user(db, user)

        if request.isSeller:
            market = Market(userId=user.userId, marketName=f"{user.firstName}'s Market")
            await UserRepository.create_market(db, market)

        token_str = create_access_token({"sub": str(user.userId)})
        token = UserToken(
            userId=user.userId,
            token=token_str,
            expiresAt=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        db.add(token)
        await db.commit()
        await db.refresh(token)

        return user, token_str

    @staticmethod
    async def login(db: AsyncSession, request):
        user = await UserRepository.get_by_login(db, request.login)
        if not user or not verify_password(request.password, user.passwordHash):
            return None, "Invalid login or password"

        token_str = create_access_token({"sub": str(user.userId)})
        token = UserToken(
            userId=user.userId,
            token=token_str,
            expiresAt=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        db.add(token)
        await db.commit()
        await db.refresh(token)

        return user, token_str