from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.controllers.product_controller import *
from app.schemas.product_schema import *
from app.schemas.response import ApiResponse
from app.security.jwt_dependency import get_current_user
from app.database.session import get_db

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("", response_model=ApiResponse[list[ProductResponse]])
async def get_my_products_endpoint(
    page: int = 1,
    limit: int = 12,
    search: str | None = None,
    category: ProductCategory | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    available: bool | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await get_my_products(
        db=db,
        user_id=user["userId"],
        page=page,
        limit=limit,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        available=available
    )

    return ApiResponse(
        data=result["items"],
        meta={
            "pagination": {
                "type": "offset",
                "offset": (page - 1) * limit,
                "limit": limit,
                "total": result["pagination"]["total"]
            }
        }
    )


@router.post("", response_model=ApiResponse[ProductResponse])
async def create_product_endpoint(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    product = await create_product(db, user["userId"], data)
    return ApiResponse(data=product)


@router.get("/{product_id}", response_model=ApiResponse[ProductResponse])
async def get_product_endpoint(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    product = await get_product(db, product_id, user["userId"])
    return ApiResponse(data=product)


@router.patch("/{product_id}", response_model=ApiResponse[ProductResponse])
async def update_product_endpoint(
    product_id: UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    product = await update_product(db, product_id, user["userId"], data)
    return ApiResponse(data=product)


@router.delete("/{product_id}", response_model=ApiResponse[None])
async def delete_product_endpoint(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    await delete_product(db, product_id, user["userId"])
    return ApiResponse(data=None)