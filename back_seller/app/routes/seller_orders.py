from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.crud import order as crud_order
from app.schemas.order import PaginatedOrdersOut, OrderStatusUpdate, SuccessResponse
from app.security.jwt_dependency import get_current_user

from app.models.order import Order, OrderStatus
from app.models.market import Market
from app.models.order_item import OrderItem

router = APIRouter(prefix="/api/seller/orders", tags=["seller"])


# GET /api/seller/orders
@router.get("", response_model=PaginatedOrdersOut)
async def list_orders(
        page: int = Query(1),
        limit: int = Query(10),
        status: str | None = Query(None),
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Market.marketId).where(
            Market.userId == current_user["userId"]
        )
    )
    market_id = result.scalar()

    if not market_id:
        return {
            "statistics": {
                "totalOrders": 0,
                "totalRevenue": 0,
                "completedOrders": 0,
                "processingOrders": 0,
                "pendingOrders": 0
            },
            "orders": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "totalItems": 0,
                "totalPages": 0
            }
        }

    return await crud_order.get_orders_with_stats(
        db, market_id, status, page, limit
    )

# GET /api/seller/orders/revenue
@router.get("/revenue")
async def get_revenue_by_orders(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Market.marketId).where(Market.userId == current_user["userId"])
    )
    market_id = result.scalar()

    if not market_id:
        return []

    result = await db.execute(
        select(
            Order.id,
            Order.createdAt,
            OrderItem.price,
            OrderItem.quantity
        )
        .join(OrderItem, OrderItem.orderId == Order.id)
        .where(Order.marketId == market_id, Order.deletedAt.is_(None))
    )

    rows = result.all()

    revenue_map = {}
    for order_id, created_at, price, qty in rows:
        if order_id not in revenue_map:
            revenue_map[order_id] = {
                "orderId": order_id,
                "date": created_at,
                "revenue": 0
            }
        revenue_map[order_id]["revenue"] += float(price) * qty

    return list(revenue_map.values())

# GET /api/seller/orders/revenue/total
@router.get("/revenue/total")
async def get_total_revenue(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Market.marketId).where(Market.userId == current_user["userId"])
    )
    market_id = result.scalar()

    if not market_id:
        return {"totalRevenue": 0}

    result = await db.execute(
        select(OrderItem.price, OrderItem.quantity)
        .join(Order, Order.id == OrderItem.orderId)
        .where(Order.marketId == market_id, Order.deletedAt.is_(None))
    )

    rows = result.all()

    total = sum(float(price) * qty for price, qty in rows)

    return {"totalRevenue": total}

# GET /api/seller/orders/completed
@router.get("/completed")
async def get_completed_orders(
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
):
    result = await db.execute(
        select(Market.marketId).where(
            Market.userId == current_user["userId"]
        )
    )
    market_id = result.scalar()

    if not market_id:
        return []

    result = await db.execute(
        select(Order).where(
            Order.marketId == market_id,
            Order.status == OrderStatus.completed,
            Order.deletedAt.is_(None)
        )
    )
    orders = result.scalars().all()

    return [
        {
            "id": order.id,
            "orderNumber": order.orderNumber,
            "totalAmount": float(order.totalAmount),
            "status": order.status,
            "deliveryAddress": order.deliveryAddress,
            "createdAt": order.createdAt
        }
        for order in orders
    ]


# PATCH /api/seller/orders/{id}/status
@router.patch("/{order_id}/status", response_model=SuccessResponse)
async def update_status(
        order_id: UUID = Path(...),
        status_update: OrderStatusUpdate = None,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):

    if status_update is None:
        raise HTTPException(400, "Status body is required")

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

    allowed_transitions = {
        OrderStatus.pending: [OrderStatus.processing, OrderStatus.cancelled],
        OrderStatus.processing: [OrderStatus.shipped, OrderStatus.cancelled],
        OrderStatus.shipped: [OrderStatus.completed],
        OrderStatus.completed: [],
        OrderStatus.cancelled: []
    }

    if status_update.status not in allowed_transitions[order.status]:
        raise HTTPException(400, "Invalid status transition")

    await crud_order.update_order_status(db, order, status_update.status)

    return {"success": True}


# DELETE /api/seller/orders/{id}
@router.delete("/{order_id}", response_model=SuccessResponse)
async def delete_order(
        order_id: UUID = Path(...),
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):

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

    return {"success": True}


# GET /api/seller/orders/{id}
@router.get("/{order_id}")
async def get_order_by_id(
        order_id: UUID = Path(...),
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
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

    result = await db.execute(
        select(OrderItem).where(OrderItem.orderId == order.id)
    )
    items = result.scalars().all()

    return {
        "id": order.id,
        "orderNumber": order.orderNumber,
        "deliveryAddress": order.deliveryAddress,
        "totalAmount": float(order.totalAmount),
        "status": order.status,
        "createdAt": order.createdAt,
        "items": [
            {
                "productId": item.productId,
                "quantity": item.quantity,
                "price": float(item.price)
            }
            for item in items
        ]
    }

