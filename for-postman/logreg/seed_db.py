import asyncio
import uuid
from datetime import datetime, timedelta

from app.db.async_session import AsyncSessionLocal
from app.models.user import User
from app.models.market import Market
from app.models.user_token import UserToken
from app.core.security import hash_password, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES


TEST_LOGIN = f"testuser_{uuid.uuid4().hex[:6]}"
TEST_PASSWORD = "password123"


async def seed():

    async with AsyncSessionLocal() as session:

        # создаём пользователя
        user = User(
            login=TEST_LOGIN,
            passwordHash=hash_password(TEST_PASSWORD),
            firstName="Test",
            lastName="User",
            patronymic=None,
            dateOfBirth=datetime(1990, 1, 1).date(),
            city="TestCity",
            telegram=None,
            isSeller=True
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        # создаём маркет
        market = Market(
            userId=user.userId,
            marketName="Test Market"
        )

        session.add(market)
        await session.commit()
        await session.refresh(market)

        # создаём токен
        token_str = create_access_token({"sub": str(user.userId)})

        token = UserToken(
            userId=user.userId,
            token=token_str,
            expiresAt=datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        session.add(token)
        await session.commit()
        await session.refresh(token)

        print("✅ Test user created")
        print("login:", TEST_LOGIN)
        print("password:", TEST_PASSWORD)
        print("userId:", user.userId)
        print("token:", token.token)


if __name__ == "__main__":
    asyncio.run(seed())