from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.market import Market


async def get_my_market(db: AsyncSession, user_id):
    result = await db.execute(
        select(Market).where(Market.userId == user_id)
    )
    market = result.scalars().first()

    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    return market


async def update_market(db: AsyncSession, user_id, data):
    result = await db.execute(
        select(Market).where(Market.userId == user_id)
    )
    market = result.scalars().first()

    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    if data.market_name is not None:
        market.marketName = data.market_name

    if data.description is not None:
        market.description = data.description

    await db.commit()
    await db.refresh(market)

    return market