from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from app.models.market import Market
from app.models.product import Product
from uuid import UUID

async def get_my_products(
        db: AsyncSession,
        user_id,
        page,
        limit,
        search,
        category,
        min_price,
        max_price,
        available
):

    result = await db.execute(
        select(Market).where(Market.userId == user_id)
    )

    market = result.scalars().first()

    if not market:
        return {
            "items": [],
            "pagination": {}
        }

    query = select(Product).where(Product.marketId == market.marketId)

    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))

    if category:
        query = query.where(Product.category == category)

    if min_price is not None:
        query = query.where(Product.price >= min_price)

    if max_price is not None:
        query = query.where(Product.price <= max_price)

    if available:
        query = query.where(Product.available > 0)

    count_query = select(func.count()).select_from(query.subquery())

    total_items = (await db.execute(count_query)).scalar()

    offset = (page - 1) * limit

    result = await db.execute(
        query.offset(offset).limit(limit)
    )

    products = result.scalars().all()

    total_pages = (total_items + limit - 1) // limit

    return {
        "items": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "totalItems": total_items,
            "totalPages": total_pages
        }
    }


async def create_product(db: AsyncSession, user_id, data):

    result = await db.execute(
        select(Market).where(Market.userId == user_id)
    )

    market = result.scalars().first()

    if not market:
        raise HTTPException(404, "Market not found")

    product = Product(
        marketId=market.marketId,
        name=data.name,
        description=data.description,
        category=data.category,
        price=data.price,
        available=data.available,
        img=data.img
    )

    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product


async def get_product(db: AsyncSession, product_id, user_id):

    product_id = UUID(str(product_id))

    result = await db.execute(
        select(Market).where(Market.userId == user_id)
    )

    market = result.scalars().first()

    if not market:
        raise HTTPException(404, "Market not found")

    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.marketId == market.marketId
        )
    )

    product = result.scalars().first()

    if not product:
        raise HTTPException(404, "Product not found")

    return product


async def update_product(db: AsyncSession, product_id, user_id, data):

    product = await get_product(db, product_id, user_id)

    if data.name is not None:
        product.name = data.name

    if data.price is not None:
        product.price = data.price

    if data.available is not None:
        product.available = data.available

    await db.commit()

    return product


async def delete_product(db: AsyncSession, product_id, user_id):

    product_id = UUID(str(product_id))

    product = await get_product(db, product_id, user_id)

    await db.delete(product)

    await db.commit()

    return True
