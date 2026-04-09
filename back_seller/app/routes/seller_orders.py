from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.crud import order as crud_order
from app.schemas.response import ApiResponse
from app.security.jwt_dependency import get_current_user

from app.models.order import Order
from app.models.market import Market

router = APIRouter(prefix="/api/v1/seller/orders", tags=["seller"])


@router.get("", response_model=ApiResponse[list])
async def list_orders(
    page: int = Query(1),
    limit: int = Query(10),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.get("isSeller"):
        raise HTTPException(403, "Only sellers allowed")

    result = await db.execute(
        select(Market.marketId).where(
            Market.userId == current_user["userId"]
        )
    )
    market_id = result.scalar()

    if not market_id:
        return ApiResponse(
            data=[],
            meta={
                "pagination": {
                    "type": "offset",
                    "offset": (page - 1) * limit,
                    "limit": limit,
                    "total": 0
                },
                "statistics": {
                    "total_orders": 0,
                    "total_revenue": 0.0,
                    "completed_orders": 0,
                    "processing_orders": 0,
                    "pending_orders": 0
                }
            }
        )

    result = await crud_order.get_orders_with_stats(
        db, market_id, status, page, limit
    )

    return ApiResponse(
        data=result["orders"],
        meta={
            "pagination": {
                "type": "offset",
                "offset": (page - 1) * limit,
                "limit": limit,
                "total": result["pagination"]["total"]
            },
            "statistics": result["statistics"]
        }
    )


@router.delete("/{order_id}", response_model=ApiResponse[None])
async def delete_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.get("isSeller"):
        raise HTTPException(403, "Only sellers allowed")

    result = await db.execute(
        select(Market.marketId).where(
            Market.userId == current_user["userId"]
        )
    )
    market_id = result.scalar()

    result = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.marketId == market_id,
            Order.deletedAt.is_(None)
        )
    )
    order = result.scalar()

    if not order:
        raise HTTPException(404, "Order not found")

    await crud_order.soft_delete_order(db, order)

    return ApiResponse(data=None)