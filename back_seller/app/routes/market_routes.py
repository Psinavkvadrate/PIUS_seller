from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import AsyncSessionLocal
from app.controllers.market_controller import get_my_market, update_market
from app.schemas.market_schema import MarketUpdate
from app.security.jwt_dependency import get_current_user


router = APIRouter(prefix="/api/markets", tags=["markets"])


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router.get("/my")
async def my_market(
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user)
):

    market = await get_my_market(db, user["userId"])

    if not market:
        return {"market": None}

    return market


@router.patch("/my")
async def update_my_market(
        data: MarketUpdate,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user)
):

    await update_market(db, user["userId"], data)

    return {"success": True}