from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.controllers.market_controller import get_my_market, update_market
from app.schemas.market_schema import MarketUpdate, MarketResponse
from app.schemas.response import ApiResponse
from app.security.jwt_dependency import get_current_user

router = APIRouter(prefix="/api/v1/markets", tags=["markets"])


@router.get("/me", response_model=ApiResponse[MarketResponse])
async def get_my_market_endpoint(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    market = await get_my_market(db, user["userId"])
    return ApiResponse(data=market)


@router.patch("/me", response_model=ApiResponse[MarketResponse])
async def update_my_market_endpoint(
    data: MarketUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    market = await update_market(db, user["userId"], data)
    return ApiResponse(data=market)