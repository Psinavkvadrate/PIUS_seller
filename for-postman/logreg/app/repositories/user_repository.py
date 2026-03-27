from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.market import Market
from sqlalchemy import select

class UserRepository:

    @staticmethod
    async def get_by_login(db: AsyncSession, login: str):
        result = await db.execute(
            select(User).filter(User.login == login)
        )
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, user: User):
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def create_market(db: AsyncSession, market: Market):
        db.add(market)
        await db.commit()
        await db.refresh(market)
        return market